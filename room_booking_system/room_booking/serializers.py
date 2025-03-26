from rest_framework import serializers
from .models import Room, RoomBooking
from django.contrib.auth import get_user_model

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username"]

class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = ['id', 'number', 'capacity']  

class RoomBookingSerializer(serializers.ModelSerializer):
    #user = serializers.StringRelatedField()  
    users = UserSerializer(many=True)
    room_id = serializers.PrimaryKeyRelatedField(queryset=Room.objects.all())  
    room = RoomSerializer(read_only=True)
    #users = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), many=True, write_only=True)

    class Meta:
        model = RoomBooking
        fields = ['id', 'room','room_id', 'start_datetime', 'end_datetime', 'users']

        extra_kwargs = {
            'user':{'read_only': True}
        }
    
    def create(self, validated_data):
        users_data = validated_data.pop("users", [])
        booking = RoomBooking.objects.create(**validated_data)  
        booking.users.set(users_data)  
        return booking