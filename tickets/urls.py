from django.urls import path
from .views import MaintenanceTicketListCreateView, MaintenanceTicketDetailView

urlpatterns = [
    path('', MaintenanceTicketListCreateView.as_view(), name='ticket_list_create'),
    path('<int:pk>/', MaintenanceTicketDetailView.as_view(), name='ticket_detail'),
]