from django.urls import path
from .views import BookingList, BookingDetailView, CancelBooking, CreateBooking

urlpatterns = [
    path('',BookingList.as_view(),name="dashboard"),
    path('booking/<int:pk>', BookingDetailView.as_view(), name = "booking-detail"),
    path('cancel/<int:booking_id>/', CancelBooking, name='cancel_booking'),
    path('create_booking/', CreateBooking.as_view(), name = 'create_booking'),
]
