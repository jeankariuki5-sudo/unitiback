from rest_framework import serializers
from .models import MaintenanceTicket

class MaintenanceTicketSerializer(serializers.ModelSerializer):
    tenant_name = serializers.ReadOnlyField(source='tenant.full_name')
    tenant_email = serializers.ReadOnlyField(source='tenant.email')
    unit_number = serializers.ReadOnlyField(source='unit.unit_number')
    property_name = serializers.ReadOnlyField(source='unit.property.name')

    class Meta:
        model = MaintenanceTicket
        fields = [
            'id', 'tenant', 'tenant_name', 'tenant_email', 
            'unit', 'unit_number', 'property_name', 
            'title', 'description', 'priority', 'status', 
            'created_at', 'updated_at'
        ]
        read_only_fields = ['tenant', 'created_at', 'updated_at']