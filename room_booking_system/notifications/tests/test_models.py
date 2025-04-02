from django.test import TestCase
from django.contrib.auth import get_user_model
from notifications.models import Notification

class NotificationModelTest(TestCase):
    def setUp(self):
        User = get_user_model()
        self.user = User.objects.create_user(username="testuser", email="test@example.com", password="testpassword")
        self.notification = Notification.objects.create(
            user=self.user,
            message="Test message",
            notification_type="booking"
        )

    def test_notification_creation(self):
        self.assertEqual(self.notification.user.username, "testuser")
        self.assertEqual(self.notification.message, "Test message")
        self.assertFalse(self.notification.is_read)

    def test_notification_str_method(self):
        self.assertEqual(str(self.notification), f"Notification for {self.user.username}: Test message")
