from django.utils import timezone
from rest_framework.test import APITestCase
from django.urls import reverse
from room_booking.models import Room, RoomBooking
from django.contrib.auth import get_user_model
from datetime import timedelta

User = get_user_model()

class RoomBookingAPITest(APITestCase):
    
    def setUp(self):
        self.user = User.objects.create_superuser(username="testuser", password="securepassword",email="test@email.com")
        self.client.force_authenticate(user=self.user)  # Authenticate the user

        self.room = Room.objects.create(number=101, capacity=5)

        self.booking_start = timezone.now() + timedelta(hours=1)
        self.booking_end = self.booking_start + timedelta(hours=2)

    def test_create_room(self):
        
        url = reverse("room-create")
        data = {"number": 102, "capacity": 10}
        response = self.client.post(url, data, format="json")

        self.assertEqual(response.status_code, 201)
        self.assertEqual(Room.objects.count(), 2)  # One from setup + new one
        self.assertEqual(Room.objects.get(number=102).capacity, 10)

    def test_create_booking(self):
        
        url = reverse("booking-list")
        data = {
            "room_id": self.room.id,
            "start_datetime": self.booking_start.strftime("%Y-%m-%dT%H:%M"),
            "end_datetime": self.booking_end.strftime("%Y-%m-%dT%H:%M"),
            "users": [self.user.id],
            "purpose": "Study Group"
        }
        response = self.client.post(url, data, format="json")

        self.assertEqual(response.status_code, 201)
        self.assertEqual(RoomBooking.objects.count(), 1)
        self.assertEqual(RoomBooking.objects.first().purpose, "Study Group")

    def test_delete_booking(self):
        
        booking = RoomBooking.objects.create(
            room=self.room,
            start_datetime=self.booking_start,
            end_datetime=self.booking_end
        )
        booking.users.add(self.user)

        url = reverse("delete-booking", kwargs={"pk": booking.id})
        response = self.client.delete(url)

        self.assertEqual(response.status_code, 204)
        self.assertEqual(RoomBooking.objects.count(), 0)  # Booking should be deleted
