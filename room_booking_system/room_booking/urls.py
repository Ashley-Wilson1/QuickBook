from django.urls import path
from .views import BookingList, BookingDetailView

urlpatterns = [
    path('',BookingList.as_view(),name="dashboard"),
    path('booking/<int:pk>', BookingDetailView.as_view(), name = "booking-detail"),
]
