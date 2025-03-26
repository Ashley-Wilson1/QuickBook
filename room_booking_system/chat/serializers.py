from rest_framework import serializers
from .models import Message
from members.models import User  

class MessageSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()  

    class Meta:
        model = Message
        fields = ["id", "user", "text", "timestamp"]

    def get_user(self, obj):
        
        return {
            "id": obj.user.id,
            "username": obj.user.username,
            "first_name": obj.user.first_name,  
            "last_name": obj.user.last_name,  
            "user_type": obj.user.user_type,
            "email": obj.user.email,  
        }
