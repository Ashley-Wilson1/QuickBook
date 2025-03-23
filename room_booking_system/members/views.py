from django.shortcuts import render
from .models import User
from rest_framework import generics
from .serializers import UserSerializer
from rest_framework.permissions import AllowAny

class CreateUserView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]  # No need for authentication during signup
