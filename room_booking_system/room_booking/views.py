from django.shortcuts import get_object_or_404
from django.utils.timezone import now
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from rest_framework import generics, status
from rest_framework.exceptions import ValidationError as DRFValidationError
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView
from datetime import datetime, time
from .models import Room, RoomBooking
from .serializers import RoomSerializer, RoomBookingSerializer, DetailedRoomBookingSerializer
from notifications.models import Notification
from notifications.tasks import send_booking_email
import pytz
from rest_framework.exceptions import PermissionDenied



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

        if not self.request.user.verified:
            raise PermissionDenied("You must be verified by an admin to book a room.")

        if self.request.user.id not in user_ids:
            user_ids.append(self.request.user.id)

        users = User.objects.filter(id__in=user_ids)
        # Convert the incoming datetime strings into timezone-aware datetimes
        local_tz = pytz.timezone("Europe/London")  
        start_datetime = local_tz.localize(datetime.strptime(start_datetime, "%Y-%m-%dT%H:%M")).astimezone(pytz.UTC)
        end_datetime = local_tz.localize(datetime.strptime(end_datetime, "%Y-%m-%dT%H:%M")).astimezone(pytz.UTC)

        # Create the RoomBooking instance
        booking = RoomBooking(
            room=requested_room,
            start_datetime=start_datetime,
            end_datetime=end_datetime,
            purpose=purpose,
        )

        try:
            # Save the booking and associate the users
            booking.save()
            booking.users.set(users)
            
            for user in users:
                Notification.objects.create(
                    user=user,
                    message=f"A new booking for '{booking.purpose}' was created.",
                    notification_type='booking'
                )

            send_booking_email.delay(booking.id, [user.id for user in users])
            print(f"Users added to booking: {[user.username for user in users]}")  # Debugging line

        except ValidationError as e:
            raise DRFValidationError({"error": e.message})

class BookingDelete(generics.DestroyAPIView):
    serializer_class = RoomBookingSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return RoomBooking.objects.filter(users=self.request.user)  # Allow any user in the booking to delete it

    def delete(self, request, *args, **kwargs):
        booking = get_object_or_404(RoomBooking, pk=kwargs["pk"])

        # Ensure the authenticated user is part of the booking
        if request.user not in booking.users.all():
            return Response({"error": "You are not authorized to cancel this booking."}, status=403)

        return super().delete(request, *args, **kwargs)


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

    def get(self, request):
        user = request.user
        current_time = now()

        current_bookings = RoomBooking.objects.filter(users=user, end_datetime__gte=current_time)
        old_bookings = RoomBooking.objects.filter(users=user, end_datetime__lt=current_time)

        return Response({
            "current_bookings": DetailedRoomBookingSerializer(current_bookings, many=True).data,
            "old_bookings": DetailedRoomBookingSerializer(old_bookings, many=True).data,
        })
class BookingDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, booking_id):
        booking = get_object_or_404(RoomBooking, id=booking_id)
        print("Booking Data:", booking)
        serializer = RoomBookingSerializer(booking)
        print("Serialized Data:", serializer.data)
        return Response(serializer.data)
    

from django.utils.timezone import localtime

class AvailableTimesView(APIView):
    def get(self, request, *args, **kwargs):
        room_id = request.query_params.get('room_id')
        date_str = request.query_params.get('date')
        duration = int(request.query_params.get('duration', 1))  # Duration state (1, 2, or 4 hours)
        
        try:
            date = datetime.strptime(date_str, "%Y-%m-%d").date()
        except ValueError:
            return Response({"error": "Invalid date format. Use YYYY-MM-DD."}, status=status.HTTP_400_BAD_REQUEST)

        booked_times = RoomBooking.objects.filter(
            room_id=room_id,
            start_datetime__date=date
        )

        local_tz = pytz.timezone("Europe/London")

        booked_slots = [
            {
                "start": localtime(booking.start_datetime).strftime("%H:%M"),
                "end": localtime(booking.end_datetime).strftime("%H:%M"),
            }
            for booking in booked_times
        ]

        available_slots = []
        for hour in range(24):
            start = time(hour)
            end = time(hour + duration) if (hour + duration) < 24 else time(23, 59)  # Adjust to 23:59

            is_available = True

            # Check if the slot overlaps with any booked time
            for slot in booked_slots:
                slot_start = datetime.strptime(slot["start"], "%H:%M").time()
                slot_end = datetime.strptime(slot["end"], "%H:%M").time()

                if (start >= slot_start and start < slot_end) or \
                   (end > slot_start and end <= slot_end) or \
                   (start <= slot_start and end >= slot_end):
                    is_available = False
                    break

            available_slots.append({
                "start": start.strftime("%H:%M"),
                "end": end.strftime("%H:%M"),
                "isAvailable": is_available
            })

        return Response(available_slots)

class BuildingListView(generics.ListAPIView):
    permission_classes = [AllowAny]

    def get(self, request):
        buildings = Room.objects.values_list('building', flat=True).distinct()
        return Response(buildings)
    
class RoomListByBuildingView(generics.ListAPIView):
    permission_classes = [AllowAny]

    def get(self, request):
        building = request.query_params.get("building")
        if not building:
            return Response({"error": "Building parameter is required."}, status=400)

        rooms = Room.objects.filter(building=building).values("id", "number", "capacity")
        return Response(rooms)