from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from .models import User
from django.conf import settings

@receiver(post_save, sender=User)
def send_verification_email(sender, instance, created, **kwargs):
    if not created and instance.verified:  
        send_mail(
            'Your Account Has Been Verified',
            'Your account has been verified by an admin. You can now book rooms.',
            settings.EMAIL_HOST_USER,  
            [instance.email],
            fail_silently=False,
        )