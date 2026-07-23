from django.urls import path
from .views import InvoiceListCreateView, InvoiceDetailView, DownloadReceiptPDFView

urlpatterns = [
    path('', InvoiceListCreateView.as_view(), name='invoice_list_create'),
    path('<int:pk>/', InvoiceDetailView.as_view(), name='invoice_detail'),
    path('payments/<int:payment_id>/receipt-pdf/', DownloadReceiptPDFView.as_view(), name='download-receipt-pdf'),
]