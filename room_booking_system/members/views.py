from django.shortcuts import render
from .models import User
from rest_framework import generics
from .serializers import UserSerializer
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from .models import User as CustomUser
from rest_framework import status
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.permissions import IsAuthenticated
from .serializers import UserSerializer

class CreateUserView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]  # No need for authentication during signup

class RetrieveUserView(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]  # Only authenticated users can access their profile

    def get_object(self):
        # Ensure the user can only access their own details
        return self.request.user

class CustomTokenObtainPairView(TokenObtainPairView):
    def post(self, request, *args, **kwargs):
        username = request.data.get("username")
        password = request.data.get("password")

        if not username or not password:
            return Response({"error": "Username and password are required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = CustomUser.objects.get(username=username)
        except CustomUser.DoesNotExist:
            return Response({"error": "Username does not exist."}, status=status.HTTP_400_BAD_REQUEST)

        # Call parent class for authentication
        response = super().post(request, *args, **kwargs)

        # If authentication fails (e.g., wrong password), return a specific error
        if response.status_code == 401:
            return Response({"error": "Incorrect password."}, status=status.HTTP_400_BAD_REQUEST)

        if response.status_code == 200:
            user.is_online = True
            user.save(update_fields=['is_online'])
            
        return response
    
class UserEmailSearchView(generics.ListAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    
    def get_queryset(self):
        
        email_query = self.request.query_params.get('email', None)
        if email_query:
            return User.objects.filter(email__icontains=email_query)  
        return User.objects.none()  
    
class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        user.is_online = False
        user.save(update_fields=['is_online'])
        return Response({"message": "User logged out successfully"}, status=200)
