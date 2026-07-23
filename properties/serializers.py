from rest_framework import serializers
from .models import Property, Unit
from tenants.models import RentAdjustmentHistory

class RentAdjustmentHistorySerializer(serializers.ModelSerializer):
    changed_by = serializers.ReadOnlyField(source='changed_by.email')

    class Meta:
        model = RentAdjustmentHistory
        fields = ['id', 'unit', 'old_rent', 'new_rent', 'changed_by', 'reason', 'changed_at']


class UnitSerializer(serializers.ModelSerializer):
    # 1. Explicitly add a write-only field so DRF generates an input box in the form
    reason = serializers.CharField(
        write_only=True, 
        required=False, 
        allow_blank=True,
        help_text="Reason for rent change (optional)"
    )

    class Meta:
        model = Unit
        fields = ['id', 'property', 'unit_number', 'rent_amount', 'is_occupied', 'reason', 'created_at']

    # 2. Extract reason in update() before saving the Unit model
    def update(self, instance, validated_data):
        reason = validated_data.pop('reason', None) or 'Standard rent adjustment'
        new_rent = validated_data.get('rent_amount', instance.rent_amount)
        old_rent = instance.rent_amount

        if new_rent != old_rent:
            request = self.context.get('request')
            user = request.user if request else None
            
            RentAdjustmentHistory.objects.create(
                unit=instance,
                old_rent=old_rent,
                new_rent=new_rent,
                changed_by=user,
                reason=reason
            )

        return super().update(instance, validated_data)


class PropertySerializer(serializers.ModelSerializer):
    units = UnitSerializer(many=True, read_only=True)
    landlord = serializers.ReadOnlyField(source='landlord.email')

    class Meta:
        model = Property
        fields = ['id', 'landlord', 'name', 'address', 'units', 'created_at']