from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import RoomBooking
from notifications.models import Notification

@receiver(post_save, sender=RoomBooking)
def send_booking_notification(sender, instance, created, **kwargs):
    if created:
        users_in_booking = instance.users.all()
        for user in users_in_booking:
            Notification.objects.create(
                user=user,
                message=f"A new booking for '{instance.purpose}' was created."
            )
