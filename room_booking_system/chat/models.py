from django.db import models
#from django.contrib.auth import get_user_model
from members.models import User
from room_booking.models import RoomBooking  




class Message(models.Model):
    booking = models.ForeignKey(RoomBooking, on_delete=models.CASCADE, related_name="messages")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}: {self.text[:20]}..."