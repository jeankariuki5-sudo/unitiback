from django.shortcuts import render

# Create your views here.
from rest_framework import generics, permissions
from .models import TenantRecord
from .serializers import TenantRecordSerializer

class TenantRecordListView(generics.ListCreateAPIView):
    serializer_class = TenantRecordSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if getattr(user, 'role', '') == 'LANDLORD':
            return TenantRecord.objects.filter(unit__property__landlord=user)
        return TenantRecord.objects.filter(user=user)