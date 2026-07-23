from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from invoicing.models import Invoice
from notifications.sms_service import send_sms_notification

class Command(BaseCommand):
    help = "Sends SMS reminders to tenants with invoices due in 3 days."

    def handle(self, *args, **options):
        today = timezone.now().date()
        target_date = today + timedelta(days=3)

        # Find all unpaid/partially paid invoices due in exactly 3 days
        upcoming_invoices = Invoice.objects.filter(
            due_date=target_date
        ).exclude(status=Invoice.Status.PAID)

        if not upcoming_invoices.exists():
            self.stdout.write(self.style.SUCCESS("No unpaid invoices due in 3 days. Skipping SMS dispatch."))
            return

        count = 0
        for invoice in upcoming_invoices:
            tenant = invoice.tenant
            phone = getattr(tenant, 'phone_number', None)

            if phone:
                balance = invoice.total_amount - invoice.amount_paid
                message = (
                    f"Hello {getattr(tenant, 'full_name', 'Tenant')}, "
                    f"this is a friendly reminder that rent of KES {balance:,.2f} "
                    f"for Unit {invoice.unit.unit_number} is due on {invoice.due_date}. "
                    f"Please settle on time to avoid late fees."
                )
                
                send_sms_notification(phone, message)
                count += 1

        self.stdout.write(self.style.SUCCESS(f"Successfully sent {count} rent reminder SMS(es)."))