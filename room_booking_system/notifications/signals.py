from django.db.models.signals import post_save
from django.dispatch import receiver
from notifications.models import Notification
from room_booking.models import RoomBooking
from chat.models import Message
from django.contrib.auth import get_user_model

User = get_user_model()

@receiver(post_save, sender=RoomBooking)
def send_booking_notification(sender, instance, created, **kwargs):
    if created:
        users = [instance.user] 
        for user in users:
            Notification.objects.create(
                user=user,
                message=f"New booking for Room {instance.room.number} from {instance.start_datetime} to {instance.end_datetime}.",
                notification_type='booking'
            )

@receiver(post_save, sender=Message)
def send_message_notification(sender, instance, created, **kwargs):
    if created:
        # Notify all users in the chat room except the sender
        users = instance.room.participants.exclude(id=instance.user.id)
        for user in users:
            Notification.objects.create(
                user=user,
                message=f"New message in Room {instance.booking.room.number} for {instance.booking.purpose}: {instance.text[:50]}...",
                notification_type='message'
            )
