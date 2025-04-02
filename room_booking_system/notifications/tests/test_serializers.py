from django.test import TestCase
from rest_framework.exceptions import ValidationError
from notifications.models import Notification
from notifications.serializers import NotificationSerializer
from django.contrib.auth import get_user_model

class NotificationSerializerTest(TestCase):
    def setUp(self):
        User = get_user_model()
        self.user = User.objects.create_user(username="testuser", email="test@example.com", password="testpassword")
        self.notification = Notification.objects.create(
            user=self.user,
            message="Test message",
            notification_type="message"
        )

    def test_notification_serializer_valid(self):
        
        serializer = NotificationSerializer(instance=self.notification)
        
        
        self.assertEqual(serializer.data["message"], "Test message")
        self.assertEqual(serializer.data["notification_type"], "message")

    def test_notification_serializer_invalid(self):
        invalid_data = {
            "user": None,  # Missing user will make it invalid
            "message": "Test message",
            "notification_type": "message"
        }
        serializer = NotificationSerializer(data=invalid_data)
        with self.assertRaises(ValidationError):
            serializer.is_valid(raise_exception=True)
