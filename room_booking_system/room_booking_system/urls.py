
from django.contrib import admin
from django.urls import path, include
from members.views import CreateUserView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include('room_booking.urls')),
    path('members/', include('django.contrib.auth.urls')),
    path('members/',include('members.urls')),
    path('members/user/register/', CreateUserView.as_view(), name = 'register'),
    path('members/token/', TokenObtainPairView.as_view(), name = 'get_token'),
    path('members/token/refresh/', TokenRefreshView.as_view(),name='refresh'),
    path('members-auth/', include('rest_framework.urls')),
]
