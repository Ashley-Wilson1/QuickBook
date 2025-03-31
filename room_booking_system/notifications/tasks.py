from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings

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
        f"Time: {booking.start_datetime.strftime('%Y-%m-%d %H:%M')} - {booking.end_datetime.strftime('%Y-%m-%d %H:%M')}\n"
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