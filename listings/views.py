from django.shortcuts import render

# Create your views here.
from rest_framework import generics, permissions, filters
from .models import PropertyListing, ListingApplication
from .serializers import PropertyListingSerializer, ListingApplicationSerializer

class PropertyListingListCreateView(generics.ListCreateAPIView):
    serializer_class = PropertyListingSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['title', 'description', 'amenities', 'unit__property__name', 'unit__property__address']

    def get_permissions(self):
        # Public users/house hunters can browse listings without logging in
        if self.request.method == 'GET':
            return [permissions.AllowAny()]
        return [permissions.IsAuthenticated()]

    def get_queryset(self):
        if self.request.method == 'GET':
            return PropertyListing.objects.filter(is_active=True, unit__is_occupied=False)
        return PropertyListing.objects.filter(unit__property__landlord=self.request.user)


class PropertyListingDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = PropertyListingSerializer

    def get_permissions(self):
        if self.request.method == 'GET':
            return [permissions.AllowAny()]
        return [permissions.IsAuthenticated()]

    def get_queryset(self):
        if self.request.method == 'GET':
            return PropertyListing.objects.filter(is_active=True)
        return PropertyListing.objects.filter(unit__property__landlord=self.request.user)


class ListingApplicationListCreateView(generics.ListCreateAPIView):
    serializer_class = ListingApplicationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if getattr(user, 'role', '') == 'LANDLORD':
            return ListingApplication.objects.filter(listing__unit__property__landlord=user)
        return ListingApplication.objects.filter(applicant=user)

    def perform_create(self, serializer):
        serializer.save(applicant=self.request.user)