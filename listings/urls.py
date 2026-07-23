from django.urls import path
from .views import (
    PropertyListingListCreateView, 
    PropertyListingDetailView, 
    ListingApplicationListCreateView
)

urlpatterns = [
    path('', PropertyListingListCreateView.as_view(), name='listing_list_create'),
    path('<int:pk>/', PropertyListingDetailView.as_view(), name='listing_detail'),
    path('applications/', ListingApplicationListCreateView.as_view(), name='application_list_create'),
]