from django.forms import ValidationError
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import ListView, FormView,DetailView,CreateView
from .models import Room, RoomBooking
from .forms import AvailabilityForm
from django.contrib import messages
from .serializers import RoomSerializer,RoomBookingSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny,IsAdminUser
from rest_framework import generics
from django.conf import settings
from rest_framework.exceptions import ValidationError as DRFValidationError
from django.contrib.auth import get_user_model
   
User = get_user_model()

class CreateBooking(generics.ListCreateAPIView):
    serializer_class = RoomBookingSerializer
    permission_classes = [IsAuthenticated]
    

    def get_queryset(self):
        return RoomBooking.objects.filter(users=self.request.user)  # Show only the user's bookings

    def perform_create(self, serializer):
        room_id = self.request.data.get("room_id")  
        start_datetime = self.request.data.get("start_datetime")
        end_datetime = self.request.data.get("end_datetime")
        user_ids = self.request.data.get("users", [])
        requested_room = get_object_or_404(Room, id=room_id)  # Ensure the room exists

        if self.request.user.id not in user_ids:
            user_ids.append(self.request.user.id)

        users = User.objects.filter(id__in=user_ids)
        
        
        booking = RoomBooking(
            room=requested_room,
            start_datetime=start_datetime,
            end_datetime=end_datetime,
        )
            

        try:
            booking.full_clean()
            booking.save()
            booking.users.set(users)
        except ValidationError as e:
            raise DRFValidationError({"error": e.message})


class BookingDelete(generics.DestroyAPIView):
    serializer_class = RoomBookingSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return RoomBooking.objects.filter(user=self.request.user)  # Show only the user's bookings

class RoomCreate(generics.CreateAPIView):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]  # Restrict to admin users

    def perform_create(self, serializer):
        serializer.save()  

class RoomDelete(generics.DestroyAPIView):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]
    


class RoomListView(generics.ListAPIView):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer
    permission_classes = [AllowAny]

class UserBookingsView(generics.ListAPIView):
    serializer_class = RoomBookingSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return RoomBooking.objects.filter(user=self.request.user)

