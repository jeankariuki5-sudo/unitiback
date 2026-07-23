from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import (
    LandlordRegisterView, 
    HouseHunterRegisterView, 
    UserProfileView,
    CreateTenantInvitationView,        
    RegisterTenantWithTokenView         
)

urlpatterns = [
    # JWT Auth
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    # Registrations
    path('register/landlord/', LandlordRegisterView.as_view(), name='register_landlord'),
    path('register/house-hunter/', HouseHunterRegisterView.as_view(), name='register_house_hunter'),
    
    # Profile Self-Service
    path('me/', UserProfileView.as_view(), name='user_profile'),

    # Invitations
    path('invite-tenant/', CreateTenantInvitationView.as_view(), name='invite_tenant'),
    path('register/tenant/', RegisterTenantWithTokenView.as_view(), name='register_tenant_token'),
]