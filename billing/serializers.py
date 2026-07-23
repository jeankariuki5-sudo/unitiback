from rest_framework import serializers
from .models import SubscriptionPlan, LandlordSubscription

class SubscriptionPlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubscriptionPlan
        fields = ['id', 'name', 'price', 'max_properties', 'max_units', 'description']


class LandlordSubscriptionSerializer(serializers.ModelSerializer):
    plan_name = serializers.ReadOnlyField(source='plan.name')
    plan_price = serializers.ReadOnlyField(source='plan.price')
    landlord_email = serializers.ReadOnlyField(source='landlord.email')

    class Meta:
        model = LandlordSubscription
        fields = ['id', 'landlord', 'landlord_email', 'plan', 'plan_name', 'plan_price', 'status', 'start_date', 'next_billing_date']
        read_only_fields = ['landlord', 'start_date']