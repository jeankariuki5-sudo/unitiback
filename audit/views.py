from django.shortcuts import render

# Create your views here.
from rest_framework import generics, permissions
from .models import AuditLog
from .serializers import AuditLogSerializer

class AuditLogListView(generics.ListAPIView):
    serializer_class = AuditLogSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if getattr(user, 'role', '') == 'LANDLORD':
            return AuditLog.objects.all().order_by('-timestamp')
        return AuditLog.objects.filter(user=user).order_by('-timestamp')