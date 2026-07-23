from django.db import models
from django.conf import settings
from properties.models import Unit

class Invoice(models.Model):
    class Status(models.TextChoices):
        UNPAID = 'UNPAID', 'Unpaid'
        PARTIALLY_PAID = 'PARTIALLY_PAID', 'Partially Paid'
        PAID = 'PAID', 'Paid'
        OVERDUE = 'OVERDUE', 'Overdue'

    unit = models.ForeignKey(Unit, on_delete=models.CASCADE, related_name='invoices')
    tenant = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='invoices'
    )
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    due_date = models.DateField()
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.UNPAID)
    allow_installments = models.BooleanField(default=False)
    number_of_installments = models.IntegerField(default=1)  # 1, 2, 3, or 4
    created_at = models.DateTimeField(auto_now_add=True)

    def remaining_balance(self):
        return self.total_amount - self.amount_paid

    def __str__(self):
        return f"Invoice #{self.id} - {self.tenant.email} ({self.status})"


class InvoiceInstallment(models.Model):
    class Status(models.TextChoices):
        PENDING = 'PENDING', 'Pending'
        PAID = 'PAID', 'Paid'
        OVERDUE = 'OVERDUE', 'Overdue'

    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE, related_name='installments')
    installment_number = models.IntegerField()  # e.g., 1 of 3
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    due_date = models.DateField()
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING)
    paid_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['installment_number']

    def __str__(self):
        return f"Invoice #{self.invoice.id} - Installment {self.installment_number} ({self.status})"