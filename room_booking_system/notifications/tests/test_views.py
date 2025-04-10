from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model
from notifications.models import Notification

class NotificationViewsTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        User = get_user_model()
        self.user = User.objects.create_user(username="testuser", email="test@example.com", password="testpassword")

        login_url = reverse("get_token")  
        response = self.client.post(login_url, {"username": "testuser", "password": "testpassword"})
        
        self.token = response.data["access"]

        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')

        self.notification = Notification.objects.create(
            user=self.user,
            message="Test message",
            notification_type="message"
        )

    def test_get_notifications(self):
        url = reverse("user-notifications")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["message"], "Test message")

    def test_mark_notification_read(self):
        url = reverse("mark-notification-read", args=[self.notification.id])
        response = self.client.patch(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.notification.refresh_from_db()
        self.assertTrue(self.notification.is_read)

    def test_mark_notification_read_not_found(self):
        url = reverse("mark-notification-read", args=[999])
        response = self.client.patch(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
