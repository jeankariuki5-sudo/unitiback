from django.urls import path
from .views import SystemHealthCheckView, LandlordDashboardStatsView


urlpatterns = [
    path('health/', SystemHealthCheckView.as_view(), name='system_health'),
    path('api/dashboard/stats/', LandlordDashboardStatsView.as_view(), name='landlord-dashboard-stats'),
]