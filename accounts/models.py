from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
import uuid


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('role', User.Role.ADMIN)

        return self.create_user(email, password, **extra_fields)

class User(AbstractUser):
    class Role(models.TextChoices):
        LANDLORD = 'LANDLORD', 'Landlord'
        TENANT = 'TENANT', 'Tenant'
        HOUSE_HUNTER = 'HOUSE_HUNTER', 'House Hunter'
        ADMIN = 'ADMIN', 'Admin'

    username = None  # Disable standard username field
    email = models.EmailField(unique=True)
    full_name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=15, unique=True)
    role = models.CharField(max_length=20, choices=Role.choices, default=Role.HOUSE_HUNTER)
    
    # Notification preferences
    notify_sms = models.BooleanField(default=True)
    notify_email = models.BooleanField(default=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['full_name', 'phone_number']

    def __str__(self):
        return f"{self.full_name} ({self.email}) - {self.role}"


class TenantInvitation(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField()
    phone_number = models.CharField(max_length=15)
    unit_id = models.IntegerField(null=True, blank=True)  # Will link to Unit model in Module 2
    is_used = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Invite for {self.email} - Token: {self.id}"