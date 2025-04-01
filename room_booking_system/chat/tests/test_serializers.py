from django.test import TestCase
from chat.models import Message
from chat.serializers import MessageSerializer
from members.models import User
from room_booking.models import Room, RoomBooking
from django.utils import timezone

class MessageSerializerTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", email="test@example.com", password="securepassword")
        self.room = Room.objects.create(number=101, capacity=10)
        self.booking = RoomBooking.objects.create(
            start_datetime=timezone.now(),
            end_datetime=timezone.now() + timezone.timedelta(hours=1),
            room=self.room,
        )
        self.booking.users.add(self.user)
        self.message = Message.objects.create(booking=self.booking, user=self.user, text="Test message")

    def test_message_serialization(self):
        serializer = MessageSerializer(instance=self.message)
        self.assertEqual(serializer.data["text"], "Test message")
        self.assertEqual(serializer.data["user"]["id"], self.user.id)
