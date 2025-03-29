import os
from celery import Celery

# Set default settings for Celery
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "room_booking_system.settings")

app = Celery("room_booking_system")

# Load settings from Django settings.py
app.config_from_object("django.conf:settings", namespace="CELERY")

# Autodiscover tasks in all installed apps
app.autodiscover_tasks()
