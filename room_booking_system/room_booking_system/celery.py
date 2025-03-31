import os
from celery import Celery
from celery.schedules import crontab


# Set default settings for Celery
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "room_booking_system.settings")

app = Celery("room_booking_system")

app.conf.beat_schedule = {
    "send_booking_reminders_every_15min": {
        "task": "notifications.tasks.send_booking_reminders",
        "schedule": crontab(minute="*/15"),  
    },
}
# Load settings from Django settings.py
app.config_from_object("django.conf:settings", namespace="CELERY")

# Autodiscover tasks in all installed apps
app.autodiscover_tasks()
