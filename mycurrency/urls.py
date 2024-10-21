"""
URL configuration for mycurrency project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from django.urls import path
from exchange.views import CurrencyExchangeRateListView,convert_currency,CurrencyListCreateView,CurrencyDetailView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('currency-rates/', CurrencyExchangeRateListView.as_view(), name='currency-rates'),
    path('convert/', convert_currency, name='convert-currency'),
    path('currencies/', CurrencyListCreateView.as_view(), name='currency-list'),
    path('currencies/<int:pk>/', CurrencyDetailView.as_view(), name='currency-detail'),
    path('v1/currency-rates/', CurrencyExchangeRateListView.as_view(), name='currency-rates-v1')
 
]
