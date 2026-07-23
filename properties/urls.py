from django.urls import path
from .views import (
    PropertyListCreateView, 
    PropertyDetailView, 
    UnitListCreateView, 
    UnitDetailView,
    RentHistoryListView
)

urlpatterns = [
    path('', PropertyListCreateView.as_view(), name='property_list_create'),
    path('<int:pk>/', PropertyDetailView.as_view(), name='property_detail'),
    path('units/', UnitListCreateView.as_view(), name='unit_list_create'),
    path('units/<int:pk>/', UnitDetailView.as_view(), name='unit_detail'),
    path('units/<int:unit_id>/rent-history/', RentHistoryListView.as_view(), name='rent_history'),
]