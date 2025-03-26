from django.urls import path
from .views import BookingMessagesListView, SendMessageView

urlpatterns = [
    path("bookings/<int:booking_id>/messages/", BookingMessagesListView.as_view(), name="booking-messages"),
    path("bookings/<int:booking_id>/messages/send/", SendMessageView.as_view(), name="send-message"),
]