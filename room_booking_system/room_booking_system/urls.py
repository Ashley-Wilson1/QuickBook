
from django.contrib import admin
from django.urls import path, include
from members.views import CreateUserView, CustomTokenObtainPairView, RetrieveUserView, UserEmailSearchView,LogoutView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('members/user/register/', CreateUserView.as_view(), name = 'register'),
    path('members/token/', CustomTokenObtainPairView.as_view(), name = 'get_token'),
    path('members/token/refresh/', CustomTokenObtainPairView.as_view(),name='refresh'),
    path("members/logout/", LogoutView.as_view(), name="logout"), 
    path('members/user/profile/', RetrieveUserView.as_view(), name='get_user_profile' ),
    path('members/user/search/', UserEmailSearchView.as_view(), name='user-email-search' ),
    path('members-auth/', include('rest_framework.urls')),
    path('room_booking/', include('room_booking.urls')),
    path('notifications/', include('notifications.urls')),
    path('chat/', include('chat.urls')),
]
