from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
from django.utils.timezone import now, timedelta, localtime
from django.utils import timezone


@shared_task
def send_booking_email(booking_id, user_ids): 
    from room_booking.models import RoomBooking
    from django.contrib.auth import get_user_model

    booking = RoomBooking.objects.get(id=booking_id)
    User = get_user_model()
    users = User.objects.filter(id__in=user_ids)

    subject = f"New Booking: {booking.purpose}"
    message = (
        f"A new booking has been created:\n\n"
        f"Room: {booking.room.number}\n"
        f"Time: {localtime(booking.start_datetime).strftime('%Y-%m-%d %H:%M')} - {localtime(booking.end_datetime).strftime('%Y-%m-%d %H:%M')}\n"
        f"Purpose: {booking.purpose}\n\n"
        f"Log in to view more details."
    )
    recipient_list = [user.email for user in users if user.email]

    if recipient_list:
        send_mail(
            subject,
            message,
            settings.EMAIL_HOST_USER,  
            recipient_list,
            fail_silently=False,
        )

@shared_task
def send_offline_message_email(message_id, user_ids, message_preview):
    from chat.models import Message
    from django.contrib.auth import get_user_model

    if not user_ids:
        return  

    message = Message.objects.get(id=message_id)  
    booking = message.booking

    User = get_user_model()
    users = User.objects.filter(id__in=user_ids) 
    recipient_list = [user.email for user in users if user.email]

    subject = f"New Message in Room {booking.room.number}"
    body = (
        f"You have a new message in the chat for '{booking.purpose}':\n\n"
        f'"{message_preview}"\n\n'
        f"Log in to QuickBook to see the full conversation."
    )
    

    if recipient_list:
        send_mail(
            subject,
            body,
            settings.EMAIL_HOST_USER,  
            recipient_list,
            fail_silently=False,
        )

@shared_task
def send_booking_reminders():
    from room_booking.models import RoomBooking

    current_time = timezone.now()  

    one_hour_start = current_time + timedelta(minutes=30)  
    one_hour_end = current_time + timedelta(hours=1.5)  

    # 1-day reminder window
    one_day_start = current_time + timedelta(hours=22.5)   
    one_day_end = current_time + timedelta(hours=25.5)     

    one_hour_bookings = RoomBooking.objects.filter(
        start_datetime__range=(one_hour_start, one_hour_end)
    )

    one_day_bookings = RoomBooking.objects.filter(
        start_datetime__range=(one_day_start, one_day_end)
    )

    for booking in one_hour_bookings | one_day_bookings:
        users = booking.users.all()
        recipient_list = [user.email for user in users if user.email]

        if recipient_list:
            time_label = "1 hour" if booking in one_hour_bookings else "1 day"
            subject = f"Reminder: Booking in {time_label}"
            message = (
                f"Your booking for room {booking.room.number} is happening in {time_label}.\n"
                f"Time: {localtime(booking.start_datetime).strftime('%Y-%m-%d %H:%M')}\n"
                f"Purpose: {booking.purpose}\n\n"
                f"Log in to view more details."
            )

            send_mail(
                subject,
                message,
                settings.EMAIL_HOST_USER,
                recipient_list,
                fail_silently=False,
            )
