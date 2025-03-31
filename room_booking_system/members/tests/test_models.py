from django.test import TestCase
from members.models import User

class UserModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="test@example.com",
            username="testuser",
            password="securepassword",
            user_type=User.STUDENT
        )

    def test_user_creation(self):
        self.assertEqual(self.user.username, "testuser")
        self.assertEqual(self.user.email, "test@example.com")
        self.assertTrue(self.user.check_password("securepassword"))

    def test_user_type_defaults_to_student(self):
        self.assertEqual(self.user.user_type, User.STUDENT)

    def test_is_student(self):
        self.assertTrue(self.user.is_student())
        self.assertFalse(self.user.is_staff_member())
