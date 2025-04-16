from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from .models import Message
from .serializers import MessageSerializer
from room_booking.models import RoomBooking
from django.http import JsonResponse
from django.views.decorators.http import require_GET
from .models import Message

class BookingMessagesListView(generics.ListAPIView):
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        booking_id = self.kwargs["booking_id"]
        return Message.objects.filter(booking_id=booking_id).order_by("timestamp")


class SendMessageView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, booking_id):
        booking = get_object_or_404(RoomBooking, id=booking_id)

        if request.user not in booking.users.all():
            return Response({"error": "You are not part of this booking"}, status=403)

        message = Message.objects.create(
            booking=booking,
            user=request.user,
            text=request.data.get("text"),
        )

        return Response(MessageSerializer(message).data)


@require_GET
def get_chat_history(request, booking_id):
    messages = Message.objects.filter(booking__id=booking_id).order_by("timestamp")
    return JsonResponse({
        "messages": [
            {
                "id": message.id,
                "user": {
                    "id": message.user.id,
                    "username": message.user.username,
                    "first_name": message.user.first_name,
                    "last_name": message.user.last_name,
                },
                "text": message.text,
                "timestamp": message.timestamp.isoformat(),
            }
            for message in messages
        ]
    })