from rest_framework.test import APITestCase
from django.urls import reverse
from members.models import User

class UserAPITest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="test@example.com",
            username="testuser",
            password="securepassword"
        )
        self.client.login(username="testuser", password="securepassword")

    def test_user_registration(self):
        url = reverse("register")
        data = {
            "username": "newuser",
            "email": "newuser@example.com",
            "password": "securepassword",
            "user_type": "student"
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data["username"], "newuser")

    def test_user_login(self):
        url = reverse("get_token")
        data = {"username": "testuser", "password": "securepassword"}
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, 200)
        self.assertIn("access", response.data)  

    def test_logout(self):
        url = reverse("logout")
        self.client.force_authenticate(user=self.user)
        response = self.client.post(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["message"], "User logged out successfully")
