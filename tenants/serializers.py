from rest_framework import serializers
from .models import TenantRecord

class TenantRecordSerializer(serializers.ModelSerializer):
    user_name = serializers.ReadOnlyField(source='user.full_name')
    user_email = serializers.ReadOnlyField(source='user.email')
    user_phone = serializers.ReadOnlyField(source='user.phone_number')

    class Meta:
        model = TenantRecord
        fields = ['id', 'user', 'user_name', 'user_email', 'user_phone', 'unit', 'move_in_date', 'created_at']