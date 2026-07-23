from rest_framework import serializers
from .models import Payment, PaymentDispute, Dispute

class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = [
            'id', 'invoice', 'amount', 'payment_method', 
            'mpesa_receipt_number', 'checkout_request_id', 
            'phone_number', 'status', 'created_at'
        ]

class ManualPaymentSerializer(serializers.Serializer):
    invoice_id = serializers.IntegerField()
    amount = serializers.DecimalField(max_digits=10, decimal_places=2)
    mpesa_receipt_number = serializers.CharField(max_length=100, required=False, allow_blank=True)

class STKPushSerializer(serializers.Serializer):
    invoice_id = serializers.IntegerField()
    phone_number = serializers.CharField(max_length=15)

class PaymentDisputeSerializer(serializers.ModelSerializer):
    tenant_email = serializers.ReadOnlyField(source='tenant.email')

    class Meta:
        model = PaymentDispute
        fields = ['id', 'tenant', 'tenant_email', 'invoice', 'reason', 'status', 'landlord_comment', 'created_at']
        read_only_fields = ['tenant', 'status', 'landlord_comment']

class DisputeSerializer(serializers.ModelSerializer):
    raised_by_email = serializers.ReadOnlyField(source='raised_by.email')

    class Meta:
        model = Dispute
        fields = [
            'id', 'payment', 'raised_by', 'raised_by_email', 
            'reason', 'status', 'resolution_notes', 'created_at', 'updated_at'
        ]
        read_only_fields = ['raised_by', 'status', 'resolution_notes', 'created_at', 'updated_at']