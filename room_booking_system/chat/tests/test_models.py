from django.test import TestCase
from chat.models import Message
from members.models import User
from room_booking.models import Room, RoomBooking
from django.utils import timezone

class MessageModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", email="test@example.com", password="securepassword")
        self.room = Room.objects.create(number=101, capacity=10)
        self.booking = RoomBooking.objects.create(
            start_datetime=timezone.now(),
            end_datetime=timezone.now() + timezone.timedelta(hours=1),
            room=self.room,
        )
        self.booking.users.add(self.user)

    def test_create_message(self):
        message = Message.objects.create(booking=self.booking, user=self.user, text="Hello, this is a test message.")
        self.assertEqual(message.text, "Hello, this is a test message.")
        self.assertEqual(message.user, self.user)
        self.assertEqual(message.booking, self.booking)
