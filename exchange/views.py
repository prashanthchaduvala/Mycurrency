from django.shortcuts import render

# Create your views here.
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import CurrencyExchangeRate, Currency
from .serializers import CurrencySerializer, CurrencyExchangeRateSerializer
from .services.exchange_service import ExchangeRateService
from django.http import JsonResponse
from datetime import datetime
from django.shortcuts import get_object_or_404
# API to list currency rates
class CurrencyExchangeRateListView(generics.ListAPIView):

    queryset = CurrencyExchangeRate.objects.all()
    serializer_class = CurrencyExchangeRateSerializer
 
    def get_queryset(self):
        # Optionally add filters based on query params (e.g., source_currency, date range)
        source_currency = self.request.query_params.get('source_currency')
        date_from = self.request.query_params.get('date_from')
        date_to = self.request.query_params.get('date_to')
 
        queryset = CurrencyExchangeRate.objects.all()
 
        if source_currency:
            queryset = queryset.filter(source_currency__code=source_currency)
        
        if date_from and date_to:
            queryset = queryset.filter(valuation_date__range=[date_from, date_to])
        
        return queryset

from datetime import date
def currency_rates_list(request):
    source_currency_code = request.GET.get('source_currency')
    date_from = request.GET.get('date_from')
    date_to = request.GET.get('date_to')

    exchange_rates = CurrencyExchangeRate.objects.filter(
        valuation_date__range=[date(2024, 1, 1), date(2024, 1, 31)]
    )
    print(exchange_rates,'-------')
    currency = Currency.objects.filter(code='USD')
    print(currency,'currencycurrency')
 
    # Validate required parameters
    if not source_currency_code or not date_from or not date_to:
        return JsonResponse({'error': 'Missing required parameters: source_currency, date_from, and date_to'}, status=400)
    
    try:
        date_from = datetime.strptime(date_from, '%Y-%m-%d').date()
        date_to = datetime.strptime(date_to, '%Y-%m-%d').date()
    except ValueError:
        return JsonResponse({'error': 'Invalid date format. Use YYYY-MM-DD'}, status=400)
 
    # Ensure the source currency exists
    source_currency = get_object_or_404(Currency, code=source_currency_code.upper())
    
    # Query the exchange rates within the date range for the source currency
    exchange_rates = CurrencyExchangeRate.objects.filter(
        source_currency=source_currency,
        valuation_date__range=[date_from, date_to]
    ).order_by('valuation_date')
    print(exchange_rates,'exchange_ratesexchange_rates')
 
    if not exchange_rates:
        return JsonResponse({'message': 'No exchange rates available for the specified criteria'}, status=404)
 
    # Prepare the response data (time series of rate values)
    rates_data = []
    for rate in exchange_rates:
        rates_data.append({
            'date': rate.valuation_date,
            'exchanged_currency': rate.exchanged_currency.code,
            'rate_value': str(rate.rate_value)  # Convert Decimal to string for JSON compatibility
        })
 
    return JsonResponse({'currency_rates': rates_data}, status=200)


import requests
def convert_currency(api_key, from_currency, to_currency, amount):
    url = 'https://api.currencybeacon.com/v1/convert'
    params = {
        'from': from_currency,
        'to': to_currency,
        'amount': amount,
        'api_key': api_key  # Add your API key here
    }
    response = requests.get(url, params=params)

    if response.status_code == 200:
        return response.json()
    else:
        return None

# # Usage example
# api_key = 'rgxHn8aJubkShWXs691HoqF26HdtYgxw'
# conversion_result = convert_currency(api_key, 'USD', 'EUR', 100)
# if conversion_result:
#     print(conversion_result)
# else:
#     print("Failed to perform conversion")



def convert_currency_view(request):
    api_key = 'rgxHn8aJubkShWXs691HoqF26HdtYgxw'
    from_currency = request.GET.get('source_currency')
    to_currency = request.GET.get('exchanged_currency')
    amount = request.GET.get('amount')
 
    if not from_currency or not to_currency or not amount:
        return JsonResponse({'error': 'Missing parameters'}, status=400)
    try:
        amount = float(amount)
    except ValueError:
        return JsonResponse({'error':'Invalid amount, please correct enter amount '},status=400)
    
    conversion_result = convert_currency(api_key, from_currency, to_currency, amount)
    
    if conversion_result:
        return JsonResponse(conversion_result)
    else:
        return JsonResponse({'error': 'Conversion failed'}, status=500)


# Currency CRUD
class CurrencyListCreateView(generics.ListCreateAPIView):
    queryset = Currency.objects.all()
    serializer_class = CurrencySerializer
 
class CurrencyDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Currency.objects.all()
    serializer_class = CurrencySerializer

from django.views import View
from .utils import fetch_and_save_exchange_rate # Assuming your fetch_and_save_exchange_rate function is in utils.py
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

@method_decorator(csrf_exempt,name='dispatch')
class UpdateExchangeRateView(View):
    api_key = 'rgxHn8aJubkShWXs691HoqF26HdtYgxw'  # Replace with your API key
 
    def get(self, request):
        # Define the currency pairs you want to fetch rates for
        currency_pairs = [('USD', 'EUR'), ('EUR', 'GBP'), ('USD', 'JPY')]
        
        for base_currency, target_currency in currency_pairs:
            fetch_and_save_exchange_rate(self.api_key, base_currency, target_currency)
        
        return JsonResponse({'status': 'Exchange rates updated.'}, status=200)

from django.http import JsonResponse
from django.views import View
from .models import CurrencyExchangeRate
from datetime import datetime
 
class CurrencyRatesListView(View):
    def get(self, request):
        source_currency_code = request.GET.get('source_currency')
        date_from = request.GET.get('date_from')
        date_to = request.GET.get('date_to')
 
        if not source_currency_code or not date_from or not date_to:
            return JsonResponse({'error': 'Missing parameters'}, status=400)
 
        try:
            date_from = datetime.strptime(date_from, '%Y-%m-%d').date()
            date_to = datetime.strptime(date_to, '%Y-%m-%d').date()
 
            exchange_rates = CurrencyExchangeRate.objects.filter(
                source_currency__code=source_currency_code,
                valuation_date__range=[date_from, date_to]
            ).order_by('valuation_date')
 
            rates_list = [
                {
                    'valuation_date': rate.valuation_date.isoformat(),
                    'rate_value': str(rate.rate_value)
                }
                for rate in exchange_rates
            ]
 
            return JsonResponse(rates_list, safe=False, status=200)
 
        except ValueError as e:
            return JsonResponse({'error': str(e)}, status=400)

