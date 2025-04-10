
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('members/', include('members.urls')),
    path('members-auth/', include('rest_framework.urls')),
    path('room_booking/', include('room_booking.urls')),
    path('notifications/', include('notifications.urls')),
    path('chat/', include('chat.urls')),
]
