from django.test import TestCase
from room_booking.models import Room, RoomBooking
from room_booking.serializers import RoomSerializer, RoomBookingSerializer
from django.contrib.auth import get_user_model
from django.utils import timezone
from datetime import timedelta

User = get_user_model()

class RoomSerializerTest(TestCase):
    def test_room_serialization(self):
        room = Room.objects.create(number=101, capacity=5, building="James Graham")
        serializer = RoomSerializer(room)
        expected_data = {"id": room.id, "number": 101, "capacity": 5, "building": "James Graham"}
        self.assertEqual(serializer.data, expected_data)

class RoomBookingSerializerTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="securepassword",email = "test@email.com")
        self.room = Room.objects.create(number=101, capacity=5)
        self.start_time = timezone.now() + timedelta(hours=1)
        self.end_time = self.start_time + timedelta(hours=2)

    def test_valid_booking_serialization(self):
        booking = RoomBooking.objects.create(
            room=self.room,
            start_datetime=self.start_time,
            end_datetime=self.end_time
        )
        booking.users.add(self.user)

        serializer = RoomBookingSerializer(booking)
        self.assertEqual(serializer.data["room"]["number"], 101)
        self.assertEqual(serializer.data["purpose"], None)
