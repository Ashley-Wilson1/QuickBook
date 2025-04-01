from django.test import TestCase
from chat.models import Message
from notifications.models import Notification
from members.models import User
from room_booking.models import Room, RoomBooking
from django.utils import timezone

class MessageSignalTest(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(username="user1", email="user1@example.com", password="securepassword")
        self.user2 = User.objects.create_user(username="user2", email="user2@example.com", password="securepassword")
        self.room = Room.objects.create(number=101, capacity=10)
        self.booking = RoomBooking.objects.create(
            start_datetime=timezone.now(),
            end_datetime=timezone.now() + timezone.timedelta(hours=1),
            room=self.room,
        )
        self.booking.users.set([self.user1, self.user2])

    def test_message_notification_signal(self):
        Message.objects.create(booking=self.booking, user=self.user1, text="Hello, test signal")
        notifications = Notification.objects.filter(user=self.user2)
        self.assertEqual(notifications.count(), 1)
        self.assertIn("New message", notifications.first().message)
