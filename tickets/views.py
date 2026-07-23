from django.shortcuts import render

# Create your views here.
from rest_framework import generics, permissions
from .models import MaintenanceTicket
from .serializers import MaintenanceTicketSerializer

class MaintenanceTicketListCreateView(generics.ListCreateAPIView):
    serializer_class = MaintenanceTicketSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if getattr(user, 'role', '') == 'LANDLORD':
            return MaintenanceTicket.objects.filter(unit__property__landlord=user)
        return MaintenanceTicket.objects.filter(tenant=user)

    def perform_create(self, serializer):
        serializer.save(tenant=self.request.user)


class MaintenanceTicketDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = MaintenanceTicketSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if getattr(user, 'role', '') == 'LANDLORD':
            return MaintenanceTicket.objects.filter(unit__property__landlord=user)
        return MaintenanceTicket.objects.filter(tenant=user)