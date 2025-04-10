from django.urls import path
from room_booking.views import CreateBooking, BookingDelete, UserBookingsView, UserBookingsView, BookingDetailView,AvailableTimesView,RoomCreate,BuildingListView, RoomListByBuildingView

urlpatterns = [
    path('bookings/',CreateBooking.as_view(),name='booking-list'),
    path("bookings/<int:booking_id>/", BookingDetailView.as_view(), name="booking-detail"),
    path('bookings/delete/<int:pk>/', BookingDelete.as_view(),name='delete-booking'),
    path("rooms/", RoomListByBuildingView.as_view(), name="room-list"),
    path("rooms/create/", RoomCreate.as_view(), name="room-create"),
    path('user/bookings/', UserBookingsView.as_view(), name='user-bookings'),
    path('available_times/', AvailableTimesView.as_view(), name='available-times'),
    path('buildings/', BuildingListView.as_view(), name='building-list'),
]
