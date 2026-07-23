from django.db import models
from django.conf import settings

class Property(models.Model):
    landlord = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='properties'
    )
    name = models.CharField(max_length=255)
    address = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.landlord.email})"


class Unit(models.Model):
    property = models.ForeignKey(
        Property, 
        on_delete=models.CASCADE, 
        related_name='units'
    )
    unit_number = models.CharField(max_length=50)  # e.g., "A1", "3B", "102"
    rent_amount = models.DecimalField(max_digits=10, decimal_places=2)
    is_occupied = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('property', 'unit_number')

    def __str__(self):
        return f"{self.property.name} - Unit {self.unit_number}"