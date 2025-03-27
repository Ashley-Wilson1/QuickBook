from django.db import models
from django.contrib.auth import models as auth_models

# Custom User Manager
class UserManager(auth_models.BaseUserManager):
    def create_user(self, email, username, password=None, user_type='student', **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, username=username, user_type=user_type, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password=None, **extra_fields):
        extra_fields.setdefault("user_type", "staff")
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        return self.create_user(email, username, password, **extra_fields)

# Custom User Model
class User(auth_models.AbstractUser):
    username = models.CharField(max_length=150, unique=True)
    first_name = models.CharField(max_length=150, blank=True)
    last_name = models.CharField(max_length=150, blank=True)
    email = models.EmailField(unique=True)
    is_online = models.BooleanField(default=False)

    STUDENT = 'student'
    STAFF = 'staff'

    USER_TYPE_CHOICES = [
        (STUDENT, 'Student'),
        (STAFF, 'Staff'),
    ]

    user_type = models.CharField(
        max_length=10,
        choices=USER_TYPE_CHOICES,
        default=STUDENT
    )

    # Custom fields
    REQUIRED_FIELDS = [ "email", "user_type"]

    objects = UserManager()  # Attach custom manager to the user model

    def is_student(self):
        return self.user_type == self.STUDENT

    def is_staff_member(self):
        return self.user_type == self.STAFF

    def __str__(self):
        return self.username


