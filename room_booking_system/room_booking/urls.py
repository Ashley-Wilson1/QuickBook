from django.urls import path
# from .views import BookingList, BookingDetailView, CancelBooking, CreateBooking
from . import views

urlpatterns = [
    # path('',BookingList.as_view(),name="dashboard"),
    # path('booking/<int:pk>', BookingDetailView.as_view(), name = "booking-detail"),
    # path('cancel/<int:booking_id>/', CancelBooking, name='cancel_booking'),
    # path('create_booking/', CreateBooking.as_view(), name = 'create_booking'),
    path('bookings/',views.CreateBooking.as_view(),name='booking-list'),
    path('bookings/delete/<int:pk>', views.BookingDelete.as_view(),name='delete-booking')
]
