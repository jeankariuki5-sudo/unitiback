from django.shortcuts import render

# Create your views here.
from django.db import connection
from django.utils import timezone
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions, status
from django.db.models import Sum, Count, Q

from invoicing.models import Invoice
from payments.models import Payment, Dispute
from properties.models import Property, Unit

class LandlordDashboardStatsView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user = request.user
        if getattr(user, 'role', '') != 'LANDLORD':
            return Response({'error': 'Only landlords can access dashboard stats.'}, status=status.HTTP_403_FORBIDDEN)

        properties = Property.objects.filter(landlord=user)
        units = Unit.objects.filter(property__in=properties)
        
        total_units = units.count()
        occupied_units = units.filter(is_occupied=True).count()
        occupancy_rate = round((occupied_units / total_units * 100), 1) if total_units > 0 else 0.0

        # Financial totals
        invoices = Invoice.objects.filter(unit__in=units)
        total_billed = invoices.aggregate(total=Sum('total_amount'))['total'] or 0
        total_collected = invoices.aggregate(total=Sum('amount_paid'))['total'] or 0
        total_outstanding = total_billed - total_collected

        # Active disputes count
        active_disputes = Dispute.objects.filter(
            payment__invoice__unit__in=units,
            status__in=['OPEN', 'UNDER_REVIEW']
        ).count()

        return Response({
            "overview": {
                "total_properties": properties.count(),
                "total_units": total_units,
                "occupied_units": occupied_units,
                "occupancy_rate_percentage": occupancy_rate
            },
            "financials": {
                "total_billed": float(total_billed),
                "total_collected": float(total_collected),
                "total_outstanding": float(total_outstanding)
            },
            "pending_actions": {
                "open_disputes": active_disputes
            }
        }, status=status.HTTP_200_OK)

class SystemHealthCheckView(APIView):
    """
    Public health check endpoint for monitoring uptime and DB status.
    """
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        try:
            connection.ensure_connection()
            db_status = "Healthy"
        except Exception:
            db_status = "Unhealthy"

        is_healthy = db_status == "Healthy"
        
        response_data = {
            "status": "UP" if is_healthy else "DOWN",
            "database": db_status,
            "timestamp": timezone.now(),
            "service": "Uniti Backend API",
            "version": "1.0.0"
        }

        return Response(
            response_data, 
            status=status.HTTP_200_OK if is_healthy else status.HTTP_503_SERVICE_UNAVAILABLE
        )