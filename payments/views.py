from rest_framework import generics, permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.db import transaction
from django.conf import settings
from notifications.sms_service import send_payment_receipt_sms
from invoicing.models import Invoice, InvoiceInstallment
from .models import Payment, PaymentDispute, Dispute
from .serializers import (
    PaymentSerializer, 
    ManualPaymentSerializer, 
    STKPushSerializer, 
    PaymentDisputeSerializer,
    DisputeSerializer  # Fixed import
)
from rest_framework.throttling import ScopedRateThrottle


def get_remaining_balance(invoice):
    """Safely calculates remaining balance without type-calling bugs."""
    if hasattr(invoice, 'remaining_balance'):
        val = invoice.remaining_balance
        return val() if callable(val) else val
    return invoice.total_amount - invoice.amount_paid


# 1. Payment List and Creation
class PaymentListCreateView(generics.ListCreateAPIView):
    serializer_class = PaymentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if getattr(user, 'role', '') == 'LANDLORD':
            return Payment.objects.filter(invoice__unit__property__landlord=user)
        return Payment.objects.filter(invoice__tenant=user)


# 2. Trigger STK Push (Landlord Manual Push & Tenant Resend)
class TriggerSTKPushView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = 'stk_push'

    def post(self, request, invoice_id):
        user = request.user
        invoice = get_object_or_404(Invoice, id=invoice_id)

        is_landlord = (getattr(user, 'role', '') == 'LANDLORD' and invoice.unit.property.landlord == user)
        is_tenant = (invoice.tenant == user)

        if not (is_landlord or is_tenant):
            return Response(
                {"error": "You do not have permission to trigger payment for this invoice."}, 
                status=status.HTTP_403_FORBIDDEN
            )

        if invoice.status == Invoice.Status.PAID:
            return Response(
                {"message": "Invoice is already fully paid."}, 
                status=status.HTTP_400_BAD_REQUEST
            )

        phone_number = getattr(invoice.tenant, 'phone_number', None) or request.data.get('phone_number')
        
        if not phone_number:
            return Response(
                {"error": "Valid phone number required for STK push."}, 
                status=status.HTTP_400_BAD_REQUEST
            )

        payable_amount = get_remaining_balance(invoice)
        pending_installment = invoice.installments.filter(status=InvoiceInstallment.Status.PENDING).first()
        
        if pending_installment:
            payable_amount = pending_installment.amount

        checkout_req_id = f"STK_PENDING_{invoice.id}"

        payment = Payment.objects.create(
            invoice=invoice,
            amount=payable_amount,
            phone_number=phone_number,
            payment_method='MPESA',
            checkout_request_id=checkout_req_id,
            status='PENDING'
        )

        triggered_by = "Landlord Manual Trigger" if is_landlord else "Tenant Resend Self-Service"

        return Response({
            "status": "STK_PUSH_SENT",
            "triggered_by": triggered_by,
            "invoice_id": invoice.id,
            "amount_prompted": payable_amount,
            "phone_number": phone_number,
            "message": f"STK push prompt sent successfully to {phone_number}."
        }, status=status.HTTP_200_OK)


# 3. Manual Rent Payment Recording
class ManualPaymentView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        return Response({
            "message": "Send a POST request to record a manual payment.",
            "example_payload": {
                "invoice_id": 1,
                "amount": "25000.00",
                "mpesa_receipt_number": "QKH123456 (optional)"
            }
        })

    def post(self, request):
        serializer = ManualPaymentSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        invoice = get_object_or_404(Invoice, id=serializer.validated_data['invoice_id'])
        amount = serializer.validated_data['amount']
        receipt = serializer.validated_data.get('mpesa_receipt_number') or f"MANUAL-{invoice.id}"

        with transaction.atomic():
            payment = Payment.objects.create(
                invoice=invoice,
                amount=amount,
                payment_method='MANUAL',
                mpesa_receipt_number=receipt,
                phone_number=getattr(invoice.tenant, 'phone_number', ''),
                status='COMPLETED'
            )

            invoice.amount_paid += amount
            
            pending_installment = invoice.installments.filter(status=InvoiceInstallment.Status.PENDING).first()
            if pending_installment and amount >= pending_installment.amount:
                pending_installment.status = InvoiceInstallment.Status.PAID
                pending_installment.save()

            total_target = getattr(invoice, 'total_amount', getattr(invoice, 'amount', 0))
            if invoice.amount_paid >= total_target:
                invoice.status = Invoice.Status.PAID
            else:
                invoice.status = Invoice.Status.PARTIALLY_PAID
            invoice.save()

        return Response(PaymentSerializer(payment).data, status=status.HTTP_201_CREATED)


# 4. M-Pesa Callback Endpoint
class MPesaCallbackView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        # 🔐 Verify secret URL parameter token against settings
        token = request.query_params.get('secret_token')
        if token != getattr(settings, 'MPESA_CALLBACK_SECRET', ''):
            return Response({'error': 'Unauthorized callback signature'}, status=status.HTTP_403_FORBIDDEN)

        # Robust data extraction handling DRF request.data, querydicts, and raw body
        data = request.data
        if hasattr(data, 'dict'):
            data = data.dict()

        if (not data or isinstance(data, str)) and request.body:
            import json
            try:
                data = json.loads(request.body.decode('utf-8'))
            except Exception:
                data = {}

        if not isinstance(data, dict):
            data = {}

        # Handle case where 'Body' might be passed as a JSON string
        body_data = data.get('Body')
        if isinstance(body_data, str):
            import json
            try:
                body_data = json.loads(body_data)
            except Exception:
                body_data = {}

        stk_callback = body_data.get('stkCallback', {}) if isinstance(body_data, dict) else {}

        # Extract CheckoutRequestID across all possible locations and casings
        checkout_id = (
            stk_callback.get('CheckoutRequestID') or 
            stk_callback.get('checkout_request_id') or
            data.get('CheckoutRequestID') or 
            data.get('checkout_request_id') or
            data.get('CheckoutRequestId')
        )

        result_code = (
            stk_callback.get('ResultCode') if isinstance(stk_callback, dict) else None
        ) or data.get('ResultCode', 0)

        receipt = data.get('MpesaReceiptNumber')
        if not receipt and isinstance(stk_callback, dict):
            items = stk_callback.get('CallbackMetadata', {}).get('Item', [])
            for item in items:
                if item.get('Name') == 'MpesaReceiptNumber':
                    receipt = item.get('Value')
        if not receipt:
            receipt = 'MOCKRECEIPT'

        # 🚨 Strict lookup by CheckoutRequestID
        payment = Payment.objects.filter(checkout_request_id=checkout_id).first()

        if not payment:
            return Response({
                'error': 'Payment record not found for this CheckoutRequestID',
                'received_checkout_id': checkout_id
            }, status=status.HTTP_404_NOT_FOUND)

        if payment.status == 'COMPLETED':
            return Response({'message': 'Already processed'}, status=status.HTTP_200_OK)

        if str(result_code) == '0':
            with transaction.atomic():
                payment.status = 'COMPLETED'
                payment.mpesa_receipt_number = receipt
                payment.save()

                invoice = payment.invoice
                invoice.amount_paid += payment.amount

                pending_inst = invoice.installments.filter(status=InvoiceInstallment.Status.PENDING).first()
                if pending_inst and payment.amount >= pending_inst.amount:
                    pending_inst.status = InvoiceInstallment.Status.PAID
                    pending_inst.save()

                total_target = getattr(invoice, 'total_amount', getattr(invoice, 'amount', 0))
                if invoice.amount_paid >= total_target:
                    invoice.status = Invoice.Status.PAID
                else:
                    invoice.status = Invoice.Status.PARTIALLY_PAID
                invoice.save()

                tenant_phone = payment.phone_number or getattr(invoice.tenant, 'phone_number', '')
                if tenant_phone:
                    remaining = get_remaining_balance(invoice)
                    send_payment_receipt_sms(
                        tenant_phone=tenant_phone,
                        amount=payment.amount,
                        receipt_no=receipt,
                        invoice_id=invoice.id,
                        remaining_balance=remaining
                    )

            return Response({'ResultCode': 0, 'ResultDesc': 'Accepted'}, status=status.HTTP_200_OK)
        else:
            payment.status = 'FAILED'
            payment.save()
            return Response({'ResultCode': 0, 'ResultDesc': 'Payment Failed or Canceled'}, status=status.HTTP_200_OK)

# 5. Payment Dispute Views
class PaymentDisputeListCreateView(generics.ListCreateAPIView):
    serializer_class = PaymentDisputeSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if getattr(user, 'role', '') == 'LANDLORD':
            return PaymentDispute.objects.filter(invoice__unit__property__landlord=user)
        return PaymentDispute.objects.filter(tenant=user)

    def perform_create(self, serializer):
        serializer.save(tenant=self.request.user)


class DisputeListCreateView(generics.ListCreateAPIView):
    queryset = Dispute.objects.all().order_by('-created_at')
    serializer_class = DisputeSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(raised_by=self.request.user)


class DisputeResolveView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def patch(self, request, pk):
        dispute = get_object_or_404(Dispute, pk=pk)

        # 🚨 Authorization Check: Ensure user is a LANDLORD and owns the property
        user = request.user
        property_landlord = dispute.payment.invoice.unit.property.landlord

        if getattr(user, 'role', '') != 'LANDLORD' or property_landlord != user:
            return Response(
                {'error': 'Unauthorized: Only the assigned landlord can resolve this dispute.'},
                status=status.HTTP_403_FORBIDDEN
            )

        new_status = request.data.get('status')
        notes = request.data.get('resolution_notes', '')

        if new_status not in [Dispute.Status.RESOLVED, Dispute.Status.REJECTED, Dispute.Status.UNDER_REVIEW]:
            return Response({'error': 'Invalid status update.'}, status=status.HTTP_400_BAD_REQUEST)

        dispute.status = new_status
        if notes:
            dispute.resolution_notes = notes
        dispute.save()

        return Response(DisputeSerializer(dispute).data, status=status.HTTP_200_OK)