from django.urls import path
from room_booking.views import CreateBooking, BookingDelete, RoomListView, UserBookingsView, UserBookingsView, BookingDetailView,AvailableTimesView

urlpatterns = [
    path('bookings/',CreateBooking.as_view(),name='booking-list'),
    path("bookings/<int:booking_id>/", BookingDetailView.as_view(), name="booking-detail"),
    path('bookings/delete/<int:pk>', BookingDelete.as_view(),name='delete-booking'),
    path("rooms/", RoomListView.as_view(), name="room-list"),
    path('user/bookings/', UserBookingsView.as_view(), name='user-bookings'),
    path('available_times/', AvailableTimesView.as_view(), name='available-times'),
]
