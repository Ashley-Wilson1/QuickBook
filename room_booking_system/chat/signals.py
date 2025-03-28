from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Message
from notifications.models import Notification

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
                message=f"New message in Room {instance.booking.room.number} for {instance.booking.purpose}: {message_preview}",
                notification_type='message'
            )
