from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Message
from notifications.models import Notification

@receiver(post_save, sender=Message)
def send_chat_notification(sender, instance, created, **kwargs):
    if created:
        chat_users = instance.booking.users.exclude(id=instance.sender.id)
        for user in chat_users:
            if not user.is_online:
                Notification.objects.create(
                    user=user,
                    message=f"New message from {instance.sender.username} in '{instance.booking.purpose}'"
                )
