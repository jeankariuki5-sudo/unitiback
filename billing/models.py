from django.db import models
from django.conf import settings

class SubscriptionPlan(models.Model):
    name = models.CharField(max_length=100)  # e.g., "Free", "Starter", "Pro"
    price = models.DecimalField(max_digits=10, decimal_places=2)
    max_properties = models.IntegerField(default=1)
    max_units = models.IntegerField(default=5)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.name} Plan - KES {self.price}"


class LandlordSubscription(models.Model):
    class Status(models.TextChoices):
        ACTIVE = 'ACTIVE', 'Active'
        EXPIRED = 'EXPIRED', 'Expired'
        CANCELLED = 'CANCELLED', 'Cancelled'

    landlord = models.OneToOneField(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='subscription'
    )
    plan = models.ForeignKey(SubscriptionPlan, on_delete=models.PROTECT)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.ACTIVE)
    start_date = models.DateField(auto_now_add=True)
    next_billing_date = models.DateField()

    def __str__(self):
        return f"{self.landlord.email} -> {self.plan.name} ({self.status})"