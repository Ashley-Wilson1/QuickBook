from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.core.mail import send_mail
from .models import User
from django.conf import settings
import logging

logger = logging.getLogger('members')

@receiver(pre_save, sender=User)
def send_verification_email(sender, instance, **kwargs):
    print("Signal triggered")
    try:
        previous_instance = User.objects.get(pk=instance.pk)
        logger.info(f"Previous verified: {previous_instance.verified}, Current verified: {instance.verified}")
    except User.DoesNotExist:
        logger.info("User does not exist yet (new user).")
        return

    if not previous_instance.verified and instance.verified:
        logger.info(f"Sending verification email to {instance.email}")
        send_mail(
            'Your Account Has Been Verified',
            'Your account has been verified by an admin. You can now book rooms.',
            settings.EMAIL_HOST_USER,
            [instance.email],
            fail_silently=False,
        )