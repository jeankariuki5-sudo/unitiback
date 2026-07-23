from rest_framework import serializers
from .models import PropertyListing, ListingApplication

class PropertyListingSerializer(serializers.ModelSerializer):
    property_name = serializers.ReadOnlyField(source='unit.property.name')
    address = serializers.ReadOnlyField(source='unit.property.address')
    unit_number = serializers.ReadOnlyField(source='unit.unit_number')
    rent_amount = serializers.ReadOnlyField(source='unit.rent_amount')

    class Meta:
        model = PropertyListing
        fields = [
            'id', 'unit', 'property_name', 'address', 'unit_number', 
            'rent_amount', 'title', 'description', 'amenities', 
            'is_active', 'created_at'
        ]


class ListingApplicationSerializer(serializers.ModelSerializer):
    applicant_name = serializers.ReadOnlyField(source='applicant.full_name')
    applicant_email = serializers.ReadOnlyField(source='applicant.email')
    applicant_phone = serializers.ReadOnlyField(source='applicant.phone_number')
    listing_title = serializers.ReadOnlyField(source='listing.title')

    class Meta:
        model = ListingApplication
        fields = [
            'id', 'listing', 'listing_title', 'applicant', 'applicant_name', 
            'applicant_email', 'applicant_phone', 'message', 'status', 'created_at'
        ]
        # Mark 'status' as read-only so applicants can't pick their own status!
        read_only_fields = ['applicant', 'status', 'created_at']