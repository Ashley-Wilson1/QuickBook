from django.utils.timezone import localtime
from django.db import models
from django.forms import ValidationError
from django.contrib.auth.models import User

class Room(models.Model):  # Automatic pk given
    number = models.IntegerField(unique=True)
    capacity = models.IntegerField()

    def __str__(self):
        return f"Room {self.number} (Capacity: {self.capacity})"

class RoomBooking(models.Model):
    start_datetime = models.DateTimeField()
    end_datetime = models.DateTimeField()
    user = models.ForeignKey(User, on_delete=models.CASCADE) 
    room = models.ForeignKey(Room, on_delete=models.CASCADE)

    def clean(self):
        # Prevent double booking for the same room
        overlapping_bookings = RoomBooking.objects.filter(
            room=self.room,
            start_datetime__lt=self.end_datetime,
            end_datetime__gt=self.start_datetime
        ).exclude(id=self.id)  # Exclude self if updating

        if overlapping_bookings.exists():
            raise ValidationError("This room is already booked for the selected time.")

    def save(self, *args, **kwargs):
        self.clean()  # Run validation before saving
        super().save(*args, **kwargs)

    def __str__(self):
        user_name = self.user.username if self.user.username else self.user.email
        start_time = localtime(self.start_datetime).strftime('%Y-%m-%d %H:%M')  # Format without +00:00
        end_time = localtime(self.end_datetime).strftime('%Y-%m-%d %H:%M')
        return f"{user_name} has booked Room {self.room.number} from {start_time} to {end_time}"

