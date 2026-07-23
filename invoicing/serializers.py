from rest_framework import serializers
from .models import Invoice

class InvoiceSerializer(serializers.ModelSerializer):
    tenant_name = serializers.ReadOnlyField(source='tenant.full_name')
    tenant_email = serializers.ReadOnlyField(source='tenant.email')
    unit_number = serializers.ReadOnlyField(source='unit.unit_number')
    property_name = serializers.ReadOnlyField(source='unit.property.name')

    class Meta:
        model = Invoice
        fields = [
            'id', 'tenant', 'tenant_name', 'tenant_email', 'unit', 
            'unit_number', 'property_name', 'amount', 'amount_paid', 
            'due_date', 'status', 'is_prorated', 'created_at'
        ]
        read_only_fields = ['amount_paid', 'status']