from django.forms import ValidationError
from rest_framework.response import Response
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import ListView, FormView,DetailView,CreateView
from .models import Room, RoomBooking
from .forms import AvailabilityForm
from django.contrib import messages
from .serializers import RoomSerializer,RoomBookingSerializer,DetailedRoomBookingSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny,IsAdminUser
from rest_framework import generics
from django.conf import settings
from rest_framework.exceptions import ValidationError as DRFValidationError
from django.contrib.auth import get_user_model
from rest_framework.views import APIView
from datetime import datetime, time
from rest_framework import status
from django.utils import timezone
import pytz

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
        purpose = self.request.data.get("purpose", "")
        requested_room = get_object_or_404(Room, id=room_id)  # Ensure the room exists

        if self.request.user.id not in user_ids:
            user_ids.append(self.request.user.id)

        users = User.objects.filter(id__in=user_ids)
        
        start_datetime = datetime.strptime(start_datetime, "%Y-%m-%dT%H:%M")
        end_datetime = datetime.strptime(end_datetime, "%Y-%m-%dT%H:%M")

        # Convert the naive datetime object to a timezone-aware datetime object in UTC using pytz
        start_datetime = timezone.make_aware(start_datetime, pytz.utc)
        end_datetime = timezone.make_aware(end_datetime, pytz.utc)

        booking = RoomBooking(
            room=requested_room,
            start_datetime=start_datetime,
            end_datetime=end_datetime,
            purpose = purpose,
        )
            

        try:
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
    serializer_class = DetailedRoomBookingSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return RoomBooking.objects.filter(users=self.request.user).prefetch_related('users')

class BookingDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, booking_id):
        booking = get_object_or_404(RoomBooking, id=booking_id)
        print("Booking Data:", booking)
        serializer = RoomBookingSerializer(booking)
        print("Serialized Data:", serializer.data)
        return Response(serializer.data)
    
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from datetime import datetime, time
from .models import RoomBooking
import pytz

class AvailableTimesView(APIView):
    def get(self, request, *args, **kwargs):
        room_id = request.query_params.get('room_id')
        date_str = request.query_params.get('date')
        duration = int(request.query_params.get('duration', 1))  # Duration state (1, 2, or 4 hours)
        
        try:
            date = datetime.strptime(date_str, "%Y-%m-%d").date()
        except ValueError:
            return Response({"error": "Invalid date format. Use YYYY-MM-DD."}, status=status.HTTP_400_BAD_REQUEST)

        # Convert to UTC timezone
        utc_zone = pytz.UTC
        date = datetime.combine(date, time.min, utc_zone)  # Start of the day in UTC

        # Query the room bookings for that day in UTC
        booked_times = RoomBooking.objects.filter(
            room_id=room_id,
            start_datetime__date=date.date(),
        )

        # Define available slots for the day in UTC
        available_slots = []
        for hour in range(24):
            start = time(hour)
            end = time(hour + duration) if (hour + duration) < 24 else time(23, 59)  # Adjust to 23:59

            is_available = True

            # Check if the slot overlaps with any booked time
            for booking in booked_times:
                if (start >= booking.start_datetime.time() and start < booking.end_datetime.time()) or \
                   (end > booking.start_datetime.time() and end <= booking.end_datetime.time()) or \
                   (start <= booking.start_datetime.time() and end >= booking.end_datetime.time()):
                    is_available = False
                    break

            available_slots.append({"start": start.strftime("%H:%M"), "end": end.strftime("%H:%M"), "isAvailable": is_available})

        return Response(available_slots)