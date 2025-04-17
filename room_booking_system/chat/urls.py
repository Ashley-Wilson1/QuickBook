from django.urls import path
from .views import BookingMessagesListView, SendMessageView,get_chat_history

urlpatterns = [
    path("bookings/<int:booking_id>/messages/", BookingMessagesListView.as_view(), name="booking-messages"),
    path("bookings/<int:booking_id>/messages/send/", SendMessageView.as_view(), name="send-message"),
    path("<int:booking_id>/history/", get_chat_history, name="chat_history"),

]