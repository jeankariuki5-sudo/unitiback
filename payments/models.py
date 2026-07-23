from django.db import models
from django.conf import settings
from invoicing.models import Invoice

class Payment(models.Model):
    class Method(models.TextChoices):
        MPESA = 'MPESA', 'M-Pesa (Daraja)'
        MANUAL = 'MANUAL', 'Manual Record'

    class Status(models.TextChoices):
        PENDING = 'PENDING', 'Pending'
        COMPLETED = 'COMPLETED', 'Completed'
        FAILED = 'FAILED', 'Failed'

    invoice = models.ForeignKey(
        Invoice, 
        on_delete=models.CASCADE, 
        related_name='payments'
    )
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=20, choices=Method.choices, default=Method.MPESA)
    
    # M-Pesa / Daraja specific fields
    mpesa_receipt_number = models.CharField(max_length=100, unique=True, null=True, blank=True)  # e.g., QKH123456
    checkout_request_id = models.CharField(max_length=255, null=True, blank=True, db_index=True) # Daraja tracking ID
    phone_number = models.CharField(max_length=15)
    
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Payment #{self.id} - KES {self.amount} ({self.status})"


class InstallmentPlan(models.Model):
    invoice = models.OneToOneField(
        Invoice, 
        on_delete=models.CASCADE, 
        related_name='installment_plan'
    )
    total_installments = models.IntegerField(default=2)
    installments_paid = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Installment Plan for Invoice #{self.invoice.id} ({self.installments_paid}/{self.total_installments} Paid)"


class PaymentDispute(models.Model):
    class DisputeStatus(models.TextChoices):
        PENDING = 'PENDING', 'Pending Review'
        RESOLVED = 'RESOLVED', 'Resolved'
        REJECTED = 'REJECTED', 'Rejected'

    tenant = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE, related_name='disputes')
    reason = models.TextField()
    status = models.CharField(max_length=20, choices=DisputeStatus.choices, default=DisputeStatus.PENDING)
    landlord_comment = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Dispute on Invoice #{self.invoice.id} by {self.tenant.email}"

class Dispute(models.Model):
    class Status(models.TextChoices):
        OPEN = 'OPEN', 'Open'
        UNDER_REVIEW = 'UNDER_REVIEW', 'Under Review'
        RESOLVED = 'RESOLVED', 'Resolved'
        REJECTED = 'REJECTED', 'Rejected'

    payment = models.ForeignKey('payments.Payment', on_delete=models.CASCADE, related_name='disputes')
    raised_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='raised_disputes')
    reason = models.TextField()
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.OPEN)
    resolution_notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Dispute #{self.id} for Payment #{self.payment_id} [{self.status}]"