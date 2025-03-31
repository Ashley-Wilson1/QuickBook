from django.urls import path
from members.views import CreateUserView,CustomTokenObtainPairView,LogoutView,RetrieveUserView,UserEmailSearchView

urlpatterns = [
    path('user/register/', CreateUserView.as_view(), name = 'register'),
    path('token/', CustomTokenObtainPairView.as_view(), name = 'get_token'),
    path('token/refresh/', CustomTokenObtainPairView.as_view(),name='refresh'),
    path("logout/", LogoutView.as_view(), name="logout"), 
    path('user/profile/', RetrieveUserView.as_view(), name='get_user_profile' ),
    path('user/search/', UserEmailSearchView.as_view(), name='user-email-search' ),
]
