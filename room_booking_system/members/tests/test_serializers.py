from django.test import TestCase
from members.serializers import UserSerializer
from members.models import User

class UserSerializerTest(TestCase):
    def test_valid_user_data(self):
        
        data = {
            "username": "newuser",
            "email": "newuser@example.com",
            "password": "securepassword",
            "user_type": "student"
        }
        serializer = UserSerializer(data=data)
        self.assertTrue(serializer.is_valid())

    def test_invalid_duplicate_username(self):
        
        User.objects.create(username="existinguser", email="user@example.com", password="securepassword")
        data = {
            "username": "existinguser",
            "email": "anotheruser@example.com",
            "password": "securepassword",
            "user_type": "student"
        }
        serializer = UserSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("username", serializer.errors)

    def test_invalid_duplicate_email(self):
        
        User.objects.create(username="user1", email="test@example.com", password="securepassword")
        data = {
            "username": "user2",
            "email": "test@example.com",
            "password": "securepassword",
            "user_type": "student"
        }
        serializer = UserSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("email", serializer.errors)
