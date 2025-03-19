from rest_framework import serializers
from .models import Room, RoomBooking

class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = ['id', 'number', 'capacity']  

class RoomBookingSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()  # Display user's username instead of ID

    class Meta:
        model = RoomBooking
        fields = ['id', 'room', 'user', 'start_datetime', 'end_datetime']

        extra_kwargs = {
            'user':{'read_only': True}
        }