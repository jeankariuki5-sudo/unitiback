from django.urls import path
from .views import SubscriptionPlanListView, LandlordSubscriptionView

urlpatterns = [
    path('plans/', SubscriptionPlanListView.as_view(), name='subscription_plans'),
    path('my-subscription/', LandlordSubscriptionView.as_view(), name='landlord_subscription'),
]