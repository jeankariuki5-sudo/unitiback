from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import TenantInvitation  # <-- Add this line

User = get_user_model()

# 1. Landlord Registration
class LandlordRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model = User
        fields = ['id', 'full_name', 'email', 'phone_number', 'password']

    def create(self, validated_data):
        validated_data['role'] = User.Role.LANDLORD
        return User.objects.create_user(**validated_data)


# 2. House Hunter Registration
class HouseHunterRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model = User
        fields = ['id', 'full_name', 'email', 'phone_number', 'password']

    def create(self, validated_data):
        validated_data['role'] = User.Role.HOUSE_HUNTER
        return User.objects.create_user(**validated_data)


# 3. User Self-Service Profile Serializer
class UserProfileSerializer(serializers.ModelSerializer):
    role = serializers.ReadOnlyField()

    class Meta:
        model = User
        fields = ['id', 'full_name', 'email', 'phone_number', 'role', 'notify_sms', 'notify_email']

# 4. Landlord creates invitation
class CreateInvitationSerializer(serializers.ModelSerializer):
    class Meta:
        model = TenantInvitation
        fields = ['id', 'email', 'phone_number', 'unit_id', 'created_at']

# 5. Tenant registers using invitation token
class TenantRegisterWithTokenSerializer(serializers.Serializer):
    token = serializers.UUIDField()
    full_name = serializers.CharField(max_length=255)
    password = serializers.CharField(write_only=True, min_length=8)

    def validate_token(self, value):
        try:
            invitation = TenantInvitation.objects.get(id=value, is_used=False)
        except TenantInvitation.DoesNotExist:
            raise serializers.ValidationError("Invalid or expired invitation token.")
        return invitation

    def create(self, validated_data):
        invitation = validated_data['token']
        
        user = User.objects.create_user(
            email=invitation.email,
            phone_number=invitation.phone_number,
            full_name=validated_data['full_name'],
            password=validated_data['password'],
            role=User.Role.TENANT
        )
        
        invitation.is_used = True
        invitation.save()
        return user