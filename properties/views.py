from django.shortcuts import render

# Create your views here.
from rest_framework import generics, permissions
from .models import Property, Unit
from .serializers import PropertySerializer, UnitSerializer, RentAdjustmentHistorySerializer
from tenants.models import RentAdjustmentHistory

class PropertyListCreateView(generics.ListCreateAPIView):
    serializer_class = PropertySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Property.objects.filter(landlord=self.request.user)

    def perform_create(self, serializer):
        serializer.save(landlord=self.request.user)


class PropertyDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = PropertySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Property.objects.filter(landlord=self.request.user)


class UnitListCreateView(generics.ListCreateAPIView):
    serializer_class = UnitSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Unit.objects.filter(property__landlord=self.request.user)


class UnitDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = UnitSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Unit.objects.filter(property__landlord=self.request.user)


class RentHistoryListView(generics.ListAPIView):
    serializer_class = RentAdjustmentHistorySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        unit_id = self.kwargs.get('unit_id')
        return RentAdjustmentHistory.objects.filter(
            unit_id=unit_id, 
            unit__property__landlord=self.request.user
        )