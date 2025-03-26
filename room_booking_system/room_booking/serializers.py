from rest_framework import serializers
from .models import Room, RoomBooking
from django.contrib.auth import get_user_model

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username','first_name', 'last_name', 'email']

class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = ['id', 'number', 'capacity']  


class RoomBookingSerializer(serializers.ModelSerializer):
    
    users = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), many=True)
    
    # Returns the full user data in the response
    users_detail = UserSerializer(source='users', many=True, read_only=True)
    
    room = RoomSerializer(read_only=True)

    class Meta:
        model = RoomBooking
        fields = ['id', 'room', 'room_id', 'start_datetime', 'end_datetime', 'users', 'users_detail']

    def create(self, validated_data):
        user_ids = validated_data.pop('users')
        booking = RoomBooking.objects.create(**validated_data)
        booking.users.set(user_ids)  
        return booking

class DetailedRoomBookingSerializer(serializers.ModelSerializer):
    room = RoomSerializer(read_only=True)
    users = UserSerializer(many=True, read_only=True)

    class Meta:
        model = RoomBooking
        fields = ['id', 'room', 'start_datetime', 'end_datetime', 'users']