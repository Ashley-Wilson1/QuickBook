from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Message
from notifications.models import Notification
from notifications.tasks import send_offline_message_email
import sys

@receiver(post_save, sender=Message)
def send_message_notification(sender, instance, created, **kwargs):
    if 'loaddata' in sys.argv:
        return

    if created:
        users = instance.booking.users.exclude(id=instance.user.id)

        message_preview = instance.text[:50] + ("..." if len(instance.text) > 50 else "")

        offline_users = users.filter(is_online=False)

        for user in users:
            Notification.objects.create(
                user=user,
                message=f"New message in Room {instance.booking.room.number} for {instance.booking.purpose}: {message_preview}",
                notification_type='message'
            )

        send_offline_message_email.delay(instance.id, list(offline_users.values_list("id", flat=True)), message_preview)