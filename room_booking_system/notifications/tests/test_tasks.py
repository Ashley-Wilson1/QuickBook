from django.test import TestCase
from unittest.mock import patch
from notifications.tasks import send_booking_email, send_offline_message_email, send_booking_reminders
from room_booking.models import RoomBooking, Room
from django.contrib.auth import get_user_model
from django.utils import timezone
from datetime import timedelta
import datetime
class NotificationTasksTest(TestCase):
    def setUp(self):
        User = get_user_model()
        self.user = User.objects.create_user(username="testuser", email="test@example.com", password="testpassword")
        
        # Create a Room instance
        self.room = Room.objects.create(number="101", capacity=10)

        # Set the booking time to match the reminder window (1 hour window)
        self.booking = RoomBooking.objects.create(
            room=self.room,
            start_datetime=timezone.make_aware(datetime.datetime(2025, 4, 1, 19, 0, 0)),  # This will fall into the 1-hour window
            end_datetime=timezone.make_aware(datetime.datetime(2025, 4, 1, 21, 0, 0)),
            purpose="Test Booking"
        )
        self.booking.users.add(self.user)

    @patch("notifications.tasks.send_mail")
    def test_send_booking_email(self, mock_send_mail):
        """Test sending a booking email"""
        send_booking_email(self.booking.id, [self.user.id])
        mock_send_mail.assert_called_once()

    @patch("notifications.tasks.send_mail")
    def test_send_offline_message_email(self, mock_send_mail):
        """Test sending an offline message email"""
        message = self.booking.messages.create(user=self.user, text="Test message")
        send_offline_message_email(message.id, [self.user.id], "Test message preview")
        mock_send_mail.assert_called_once()

    @patch("notifications.tasks.send_mail")
    def test_send_booking_reminders(self, mock_send_mail):
        """Test sending booking reminders"""
        # Create a booking that falls within the 1-hour reminder window
        current_time = timezone.now()
        start_time = current_time + timedelta(minutes=45)  # 45 minutes from now
        end_time = start_time + timedelta(hours=1)

        booking = RoomBooking.objects.create(
            room=self.room,
            start_datetime=start_time,
            end_datetime=end_time,
            purpose="Reminder Test"
        )
        booking.users.add(self.user)

        # Call the task
        send_booking_reminders()

        # Assert that send_mail was called
        mock_send_mail.assert_called_once()
        call_args = mock_send_mail.call_args
        self.assertIn("Reminder: Booking in 1 hour", call_args[0][0])  # Subject
        self.assertIn("Reminder Test", call_args[0][1])  # Message body
