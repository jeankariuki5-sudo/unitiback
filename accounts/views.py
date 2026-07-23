from django.shortcuts import render

# Create your views here.
from rest_framework import generics, permissions
from django.contrib.auth import get_user_model
from .models import TenantInvitation
from .serializers import (
    LandlordRegisterSerializer, 
    HouseHunterRegisterSerializer, 
    UserProfileSerializer,
    CreateInvitationSerializer, 
    TenantRegisterWithTokenSerializer
)

User = get_user_model()

class LandlordRegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = LandlordRegisterSerializer
    permission_classes = [permissions.AllowAny]

class HouseHunterRegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = HouseHunterRegisterSerializer
    permission_classes = [permissions.AllowAny]

class UserProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user

# Ensure this view class is present in views.py:
class CreateTenantInvitationView(generics.CreateAPIView):
    queryset = TenantInvitation.objects.all()
    serializer_class = CreateInvitationSerializer
    permission_classes = [permissions.IsAuthenticated]

# Ensure this view class is present in views.py:
class RegisterTenantWithTokenView(generics.CreateAPIView):
    serializer_class = TenantRegisterWithTokenSerializer
    permission_classes = [permissions.AllowAny]
