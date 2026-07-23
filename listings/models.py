from django.db import models
from django.conf import settings
from properties.models import Unit

class PropertyListing(models.Model):
    unit = models.OneToOneField(
        Unit, 
        on_delete=models.CASCADE, 
        related_name='listing'
    )
    title = models.CharField(max_length=255)
    description = models.TextField()
    amenities = models.TextField(
        help_text="Comma-separated list (e.g., WiFi, Parking, Balcony, Security)", 
        blank=True
    )
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Listing: {self.title} - Unit {self.unit.unit_number}"


class ListingApplication(models.Model):
    class Status(models.TextChoices):
        PENDING = 'PENDING', 'Pending'
        APPROVED = 'APPROVED', 'Approved'
        REJECTED = 'REJECTED', 'Rejected'

    listing = models.ForeignKey(
        PropertyListing, 
        on_delete=models.CASCADE, 
        related_name='applications'
    )
    applicant = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='listing_applications'
    )
    message = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Application by {self.applicant.email} for {self.listing.title}"