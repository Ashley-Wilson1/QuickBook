from django.test import TestCase
from django.utils import timezone
from datetime import timedelta
from django.contrib.auth import get_user_model
from room_booking.models import Room, RoomBooking
from django.utils.timezone import localtime

User = get_user_model()

class RoomModelTest(TestCase):
    def test_create_room(self):
        room = Room.objects.create(number=101, capacity=5)
        self.assertEqual(room.number, 101)
        self.assertEqual(room.capacity, 5)
        self.assertEqual(str(room), "Room 101 (Capacity: 5)")

class RoomBookingModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="securepassword", email="test@email.com")
        self.room = Room.objects.create(number=101, capacity=5)
        self.start_time = timezone.now() + timedelta(hours=1)
        self.end_time = self.start_time + timedelta(hours=2)

    def test_create_booking(self):
        # Create a booking
        booking = RoomBooking.objects.create(
            room=self.room,
            start_datetime=self.start_time,
            end_datetime=self.end_time,
            purpose="Team Meeting"
        )
        booking.users.add(self.user)

        # Assert the booking was created
        self.assertEqual(RoomBooking.objects.count(), 1)
        self.assertIn(self.user, booking.users.all())

        self.assertEqual(booking.purpose, "Team Meeting")

        local_start_time = localtime(self.start_time).strftime('%Y-%m-%d %H:%M')
        local_end_time = localtime(self.end_time).strftime('%Y-%m-%d %H:%M')
        expected_str = f"Room {self.room.number} booked from {local_start_time} to {local_end_time}"
        self.assertEqual(str(booking), expected_str)

        # Assert the start and end times are correctly stored
        self.assertEqual(booking.start_datetime, self.start_time)
        self.assertEqual(booking.end_datetime, self.end_time)

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
