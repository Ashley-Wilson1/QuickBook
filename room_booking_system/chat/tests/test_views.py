from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from chat.models import Message
from members.models import User
from room_booking.models import Room, RoomBooking
from django.utils import timezone

class ChatViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username="testuser", email="test@example.com", password="securepassword")
        self.room = Room.objects.create(number=101, capacity=10)
        self.booking = RoomBooking.objects.create(
            start_datetime=timezone.now(),
            end_datetime=timezone.now() + timezone.timedelta(hours=1),
            room=self.room,
        )
        self.booking.users.add(self.user)
        self.message = Message.objects.create(booking=self.booking, user=self.user, text="Test message")
        self.client.force_authenticate(user=self.user)

    def test_get_booking_messages(self):
        url = reverse("booking-messages", kwargs={"booking_id": self.booking.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["text"], "Test message")

    def test_send_message(self):
        url = reverse("send-message", kwargs={"booking_id": self.booking.id})
        data = {"text": "New message"}
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["text"], "New message")
