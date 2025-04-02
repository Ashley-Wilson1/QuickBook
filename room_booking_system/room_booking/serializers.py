from rest_framework import serializers
from .models import Room, RoomBooking
from django.contrib.auth import get_user_model
from django.utils.timezone import localtime

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
    room = RoomSerializer(read_only=True)
    users_detail = UserSerializer(source='users', many=True, read_only=True)  # Add this field

    formatted_start_datetime = serializers.SerializerMethodField()
    formatted_end_datetime = serializers.SerializerMethodField()

    class Meta:
        model = RoomBooking
        fields = ['id', 'room', 'start_datetime', 'end_datetime', 
                  'formatted_start_datetime', 'formatted_end_datetime', 'users', 'users_detail', 'purpose']

    def get_formatted_start_datetime(self, obj):
        # Handle both model instance and dictionary cases
        start_datetime = obj.start_datetime if isinstance(obj, RoomBooking) else obj['start_datetime']
        return localtime(start_datetime).strftime("%Y-%m-%d %H:%M")

    def get_formatted_end_datetime(self, obj):
        end_datetime = obj.end_datetime if isinstance(obj, RoomBooking) else obj['end_datetime']
        return localtime(end_datetime).strftime("%Y-%m-%d %H:%M")

    def create(self, validated_data):
        user_ids = validated_data.pop('users')
        booking = RoomBooking.objects.create(**validated_data)
        booking.users.set(user_ids)  
        return booking

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        
        if isinstance(instance, RoomBooking):
            # If instance is a model, convert to local time
            representation['start_datetime'] = localtime(instance.start_datetime).isoformat()
            representation['end_datetime'] = localtime(instance.end_datetime).isoformat()
        else:
            # If instance is a dictionary, access fields directly
            representation['start_datetime'] = localtime(instance['start_datetime']).isoformat()
            representation['end_datetime'] = localtime(instance['end_datetime']).isoformat()
        
        return representation

class DetailedRoomBookingSerializer(serializers.ModelSerializer):
    room = RoomSerializer(read_only=True)
    users = UserSerializer(many=True, read_only=True)

    start_datetime = serializers.DateTimeField()
    end_datetime = serializers.DateTimeField()
    formatted_start_datetime = serializers.SerializerMethodField()
    formatted_end_datetime = serializers.SerializerMethodField()

    class Meta:
        model = RoomBooking
        fields = ['id', 'room', 'start_datetime', 'end_datetime', 
                  'formatted_start_datetime', 'formatted_end_datetime', 'users', 'purpose']

    def get_formatted_start_datetime(self, obj):
        
        return localtime(obj.start_datetime).strftime("%Y-%m-%d %H:%M")

    def get_formatted_end_datetime(self, obj):
        return localtime(obj.end_datetime).strftime("%Y-%m-%d %H:%M")

