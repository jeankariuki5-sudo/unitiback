from django.urls import path
from .views import TenantRecordListView

urlpatterns = [
    path('', TenantRecordListView.as_view(), name='tenant_record_list_create'),
]