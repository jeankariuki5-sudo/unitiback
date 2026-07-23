"""
URL configuration for unitiback project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('management-portal-secure-x89/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path('api/accounts/', include('accounts.urls')),
    path('api/properties/', include('properties.urls')),
    path('api/tenants/', include('tenants.urls')),
    path('api/invoicing/', include('invoicing.urls')),
    path('api/payments/', include('payments.urls')),
    path('api/tickets/', include('tickets.urls')),
    path('api/listings/', include('listings.urls')),
    path('api/notifications/', include('notifications.urls')),
    path('api/audit/', include('audit.urls')),
    path('api/billing/', include('billing.urls')),
    path('api/core/', include('core.urls')),
]