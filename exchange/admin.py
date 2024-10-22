from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Provider
from .services.exchange_service import ExchangeRateService
from django.urls import path
from django.shortcuts import render
from .models import Currency, CurrencyExchangeRate

@admin.register(Provider)
class ProviderAdmin(admin.ModelAdmin):
    list_display = ('name', 'priority', 'active')
    list_editable = ('priority', 'active')

@admin.register(Currency)
class CurrencyAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', 'symbol')  # Columns to display in the list view
    search_fields = ('code', 'name')  # Fields to search
 
@admin.register(CurrencyExchangeRate)
class CurrencyExchangeRateAdmin(admin.ModelAdmin):
    list_display = ('source_currency', 'exchanged_currency', 'valuation_date', 'rate_value')  # Columns to display
    list_filter = ('source_currency', 'exchanged_currency', 'valuation_date')  # Filters for the list view
    search_fields = ('source_currency__code', 'exchanged_currency__code')  # Search fields

class ConverterAdmin(admin.ModelAdmin):
    change_list_template = "admin/converter_view.html"
 
    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('converter/', self.admin_site.admin_view(self.converter_view)),
        ]
        return custom_urls + urls
 
    def converter_view(self, request):
        context = {}
        if request.method == 'POST':
            source_currency = request.POST.get('source_currency')
            target_currencies = request.POST.getlist('target_currencies')
            amount = float(request.POST.get('amount'))
            
            service = ExchangeRateService()
            results = []
            for target_currency in target_currencies:
                rate = service.get_exchange_rate(source_currency, target_currency, None)
                converted_amount = rate * amount if rate else None
                results.append({'currency': target_currency, 'rate': rate, 'converted_amount': converted_amount})
            context['results'] = results
 
        return render(request, 'admin/converter_view.html', context)

