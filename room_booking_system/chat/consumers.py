from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
import json

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):

        self.booking_id = self.scope["url_route"]["kwargs"]["booking_id"]
        self.room_group_name = f"chat_{self.booking_id}"

        self.scope["user"] = await self.authenticate_user()

        if self.scope["user"].is_anonymous:
            await self.close()
        else:
            await self.channel_layer.group_add(
                self.room_group_name,
                self.channel_name
            )
            await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )


    async def receive(self, text_data):
        from .models import Message

        print("Message received from WebSocket:", text_data) 
        try:
            data = json.loads(text_data)
            message_text = data.get("text")  
            user = self.scope["user"]

            if user.is_anonymous:
                await self.send(text_data=json.dumps({
                    "error": "User is not authenticated."
                }))
                return

            await self.save_message(user, message_text)

            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    "type": "chat_message",
                    "message": message_text,
                    "user": {
                        "id": user.id,
                        "username": user.username,
                        "first_name": user.first_name,
                        "last_name": user.last_name,
                    },
                }
            )
        except Exception as e:
            await self.close()

    @database_sync_to_async
    def save_message(self, user, message_text):
        from .models import Message  
        Message.objects.create(
            booking_id=self.scope["url_route"]["kwargs"]["booking_id"],  
            user=user,
            text=message_text
        )

    async def chat_message(self, event):
        try:
            await self.send(text_data=json.dumps({
                "text": event["message"],
                "user": event["user"],
            }))
        except Exception as e:
            await self.close()    

    @database_sync_to_async
    def authenticate_user(self):
        from django.contrib.auth.models import AnonymousUser
        from django.contrib.auth import get_user_model
        from rest_framework_simplejwt.tokens import UntypedToken
        from rest_framework_simplejwt.exceptions import InvalidToken, TokenError

        User = get_user_model()

        query_string = self.scope["query_string"].decode()
        token = dict(x.split("=") for x in query_string.split("&")).get("token")
        try:
            validated_token = UntypedToken(token)
            user_id = validated_token["user_id"]
            return User.objects.get(id=user_id)
        except (InvalidToken, TokenError, User.DoesNotExist):
            return AnonymousUser()