from django.db import models
from django.conf import settings
from properties.models import Unit

class TenantRecord(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='tenant_record'
    )
    unit = models.ForeignKey(
        Unit, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name='tenants'
    )
    move_in_date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Tenant: {self.user.full_name} -> {self.unit}"


class RentAdjustmentHistory(models.Model):
    unit = models.ForeignKey(
        Unit, 
        on_delete=models.CASCADE, 
        related_name='rent_adjustments'
    )
    old_rent = models.DecimalField(max_digits=10, decimal_places=2)
    new_rent = models.DecimalField(max_digits=10, decimal_places=2)
    changed_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    reason = models.CharField(max_length=255, blank=True, null=True)
    changed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.unit}: KES {self.old_rent} -> KES {self.new_rent}"