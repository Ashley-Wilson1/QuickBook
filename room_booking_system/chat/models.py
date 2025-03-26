from django.db import models
from django.contrib.auth import get_user_model
from room_booking.models import RoomBooking  


User = get_user_model()

class Message(models.Model):
    booking = models.ForeignKey(RoomBooking, on_delete=models.CASCADE, related_name="messages")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}: {self.text[:20]}..."