from django.db.models.signals import post_save
from django.dispatch import receiver
from notifications.models import Notification
from room_booking.models import RoomBooking
from chat.models import Message
from django.contrib.auth import get_user_model
from django.utils.timezone import localtime

User = get_user_model()

@receiver(post_save, sender=RoomBooking)
def send_booking_notification(sender, instance, created, **kwargs):
    if created:
        users_in_booking = instance.users.all()  

        start_time = localtime(instance.start_datetime).strftime('%Y-%m-%d %H:%M')
        end_time = localtime(instance.end_datetime).strftime('%Y-%m-%d %H:%M')

        for user in users_in_booking:
            Notification.objects.create(
                user=user,
                message=f"New booking for Room {instance.room.number} for {instance.booking.purpose} from {start_time} to {end_time}.",
                notification_type='booking'
            )

@receiver(post_save, sender=Message)
def send_message_notification(sender, instance, created, **kwargs):
    if created:
        # Notify all users in the chat room except the sender
        users = instance.booking.users.exclude(id=instance.user.id)  # Assuming 'room' is a field on Message

        # Truncate message preview to the first 50 characters
        message_preview = instance.text[:50] + ("..." if len(instance.text) > 50 else "")

        for user in users:
            Notification.objects.create(
                user=user,
                message=f"New message in Room {instance.booking.room.number} for {instance.booking.room.purpose}: {message_preview}",
                notification_type='message'
            )
