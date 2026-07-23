from django.shortcuts import render

# Create your views here.
from rest_framework import generics, permissions
from .models import SubscriptionPlan, LandlordSubscription
from .serializers import SubscriptionPlanSerializer, LandlordSubscriptionSerializer

class SubscriptionPlanListView(generics.ListAPIView):
    queryset = SubscriptionPlan.objects.all()
    serializer_class = SubscriptionPlanSerializer
    permission_classes = [permissions.AllowAny]


class LandlordSubscriptionView(generics.RetrieveUpdateAPIView):
    serializer_class = LandlordSubscriptionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        subscription, _ = LandlordSubscription.objects.get_or_create(
            landlord=self.request.user,
            defaults={
                'plan': SubscriptionPlan.objects.first(),
                'next_billing_date': '2026-12-31'
            }
        )
        return subscription