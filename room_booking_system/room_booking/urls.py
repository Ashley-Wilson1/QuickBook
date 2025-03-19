from django.urls import path
from .views import BookingList, BookingDetailView, cancel_booking

urlpatterns = [
    path('',BookingList.as_view(),name="dashboard"),
    path('booking/<int:pk>', BookingDetailView.as_view(), name = "booking-detail"),
    path('cancel/<int:booking_id>/', cancel_booking, name='cancel_booking'),
]
