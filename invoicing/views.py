from django.shortcuts import render

# Create your views here.
from rest_framework import generics, permissions
from .models import Invoice
from .serializers import InvoiceSerializer
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework import permissions, status
from weasyprint import HTML

from payments.models import Payment

class DownloadReceiptPDFView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, payment_id):
        payment = get_object_or_404(Payment, id=payment_id)
        invoice = payment.invoice

        # Permission check: Only tenant owner or landlord can download
        is_landlord = (getattr(request.user, 'role', '') == 'LANDLORD' and invoice.unit.property.landlord == request.user)
        is_tenant = (invoice.tenant == request.user)

        if not (is_landlord or is_tenant):
            return HttpResponse("Unauthorized", status=403)

        # Render HTML template with context
        html_string = render_to_string('invoicing/receipt.html', {
            'payment': payment,
            'invoice': invoice,
        })

        # Generate PDF
        pdf_file = HTML(string=html_string).write_pdf()

        response = HttpResponse(pdf_file, content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="Receipt_Invoice_{invoice.id}_{payment.mpesa_receipt_number}.pdf"'
        return response

class InvoiceListCreateView(generics.ListCreateAPIView):
    serializer_class = InvoiceSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if getattr(user, 'role', '') == 'LANDLORD':
            return Invoice.objects.filter(unit__property__landlord=user)
        return Invoice.objects.filter(tenant=user)


class InvoiceDetailView(generics.RetrieveUpdateAPIView):
    serializer_class = InvoiceSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if getattr(user, 'role', '') == 'LANDLORD':
            return Invoice.objects.filter(unit__property__landlord=user)
        return Invoice.objects.filter(tenant=user)