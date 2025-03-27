from django.urls import path
from .views import UserNotificationsView, MarkNotificationReadView

urlpatterns = [
    path("user/", UserNotificationsView.as_view(), name="user-notifications"),
    path("<int:pk>/read/", MarkNotificationReadView.as_view(), name="mark-notification-read"),
]
