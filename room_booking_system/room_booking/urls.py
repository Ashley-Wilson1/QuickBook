from django.urls import path
from room_booking.views import CreateBooking, BookingDelete, RoomListView, UserBookingsView, UserBookingsView

urlpatterns = [
    path('bookings/',CreateBooking.as_view(),name='booking-list'),
    path('bookings/delete/<int:pk>', BookingDelete.as_view(),name='delete-booking'),
    path("rooms/", RoomListView.as_view(), name="room-list"),
    path('user/bookings/', UserBookingsView.as_view(), name='user-bookings'),
]
