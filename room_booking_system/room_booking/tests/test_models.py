from django.test import TestCase
from django.utils import timezone
from room_booking.models import Room, RoomBooking
from django.contrib.auth import get_user_model
from datetime import timedelta

User = get_user_model()

class RoomModelTest(TestCase):
    def test_create_room(self):
        room = Room.objects.create(number=101, capacity=5)
        self.assertEqual(room.number, 101)
        self.assertEqual(room.capacity, 5)
        self.assertEqual(str(room), "Room 101 (Capacity: 5)")

class RoomBookingModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="securepassword",email="test@email.com")
        self.room = Room.objects.create(number=101, capacity=5)
        self.start_time = timezone.now() + timedelta(hours=1)
        self.end_time = self.start_time + timedelta(hours=2)

    def test_create_booking(self):
        booking = RoomBooking.objects.create(
            room=self.room,
            start_datetime=self.start_time,
            end_datetime=self.end_time
        )
        booking.users.add(self.user)

        self.assertEqual(RoomBooking.objects.count(), 1)
        self.assertIn(self.user, booking.users.all())
        self.assertEqual(str(booking), f"Room 101 booked from {self.start_time.strftime('%Y-%m-%d %H:%M')} to {self.end_time.strftime('%Y-%m-%d %H:%M')}")

    def test_double_booking_not_allowed(self):
        RoomBooking.objects.create(
            room=self.room,
            start_datetime=self.start_time,
            end_datetime=self.end_time
        )

        with self.assertRaises(Exception):  # Should raise ValidationError
            RoomBooking.objects.create(
                room=self.room,
                start_datetime=self.start_time,
                end_datetime=self.end_time
            )
