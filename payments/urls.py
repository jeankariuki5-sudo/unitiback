from django.urls import path
from .views import (
    PaymentListCreateView,
    ManualPaymentView, 
    TriggerSTKPushView, 
    MPesaCallbackView, 
    PaymentDisputeListCreateView,
    DisputeListCreateView, 
    DisputeResolveView
)

urlpatterns = [
    path('', PaymentListCreateView.as_view(), name='payment_list_create'),
    path('manual/', ManualPaymentView.as_view(), name='manual_payment'),
    path('trigger-stk/<int:invoice_id>/', TriggerSTKPushView.as_view(), name='trigger_stk_push'),
    path('callback/', MPesaCallbackView.as_view(), name='mpesa_callback'),
    path('mpesa-callback/', MPesaCallbackView.as_view(), name='mpesa_callback_legacy'),
    path('disputes/', DisputeListCreateView.as_view(), name='dispute-list-create'),
    path('disputes/<int:pk>/resolve/', DisputeResolveView.as_view(), name='dispute-resolve'),
]