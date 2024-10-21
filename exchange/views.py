from django.shortcuts import render

# Create your views here.
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import CurrencyExchangeRate, Currency
from .serializers import CurrencySerializer, CurrencyExchangeRateSerializer
from .services.exchange_service import ExchangeRateService
 
# API to list currency rates
class CurrencyExchangeRateListView(generics.ListAPIView):
    serializer_class = CurrencyExchangeRateSerializer
 
    def get_queryset(self):
        source_currency = self.request.query_params.get('source_currency')
        date_from = self.request.query_params.get('date_from')
        date_to = self.request.query_params.get('date_to')
        return CurrencyExchangeRate.objects.filter(source_currency=source_currency, valuation_date__range=[date_from, date_to])
 
# API to convert amount between currencies
@api_view(['GET'])
def convert_currency(request):
    source_currency = request.query_params.get('source_currency')
    exchanged_currency = request.query_params.get('exchanged_currency')
    amount = float(request.query_params.get('amount'))
 
    service = ExchangeRateService()
    rate = service.get_exchange_rate(source_currency, exchanged_currency, valuation_date=None)
 
    if rate:
        converted_amount = rate * amount
        return Response({"converted_amount": converted_amount, "rate": rate})
    return Response({"error": "Unable to fetch rate"}, status=400)
 
# Currency CRUD
class CurrencyListCreateView(generics.ListCreateAPIView):
    queryset = Currency.objects.all()
    serializer_class = CurrencySerializer
 
class CurrencyDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Currency.objects.all()
    serializer_class = CurrencySerializer
