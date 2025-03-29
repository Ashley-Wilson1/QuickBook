from rest_framework.generics import ListAPIView, UpdateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Notification
from .serializers import NotificationSerializer
from django.conf import settings
from django.core.mail import send_mail

class UserNotificationsView(ListAPIView):
    serializer_class = NotificationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Notification.objects.filter(user=self.request.user, is_read=False)


class MarkNotificationReadView(UpdateAPIView):
    serializer_class = NotificationSerializer
    permission_classes = [IsAuthenticated]

    def patch(self, request, pk):
        try:
            notification = Notification.objects.get(pk=pk, user=request.user)
            notification.is_read = True
            notification.save(update_fields=["is_read"])
            return Response({"message": "Notification marked as read"})
        except Notification.DoesNotExist:
            return Response({"error": "Notification not found"}, status=404)

class SendNotifications():
    def send_booking_email(booking, users): 
        subject = f"New Booking: {booking.purpose}"
        message = (
            f"A new booking has been created:\n\n"
            f"Room: {booking.room.number}\n"
            f"Time: {booking.start_datetime.strftime('%Y-%m-%d %H:%M')} - {booking.end_datetime.strftime('%Y-%m-%d %H:%M')}\n"
            f"Purpose: {booking.purpose}\n\n"
            f"Log in to view more details."
        )
        recipient_list = [user.email for user in users if user.email]

        if recipient_list:
            send_mail(
                subject,
                message,
                settings.EMAIL_HOST_USER,  # From email
                recipient_list,
                fail_silently=False,
            )

    def send_offline_message_email(message, users, message_preview):
        if not users:
            return  

        subject = f"New Message in Room {message.booking.room.number}"
        body = (
            f"You have a new message in the chat for '{message.booking.purpose}':\n\n"
            f'"{message_preview}"\n\n'
            f"Log in to QuickBook to see the full conversation."
        )
        
        recipient_list = [user.email for user in users if user.email]

        if recipient_list:
            send_mail(
                subject,
                body,
                settings.EMAIL_HOST_USER,  
                recipient_list,
                fail_silently=False,
            )