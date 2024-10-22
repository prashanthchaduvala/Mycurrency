import requests
from decimal import Decimal
from datetime import date
from django.core.exceptions import ObjectDoesNotExist
from .models import Currency, CurrencyExchangeRate
 
def fetch_and_save_exchange_rate(api_key, base_currency_code, target_currency_code):
    url = 'https://api.currencybeacon.com/v1/convert'
    params = {
        'from': base_currency_code,
        'to': target_currency_code,
        'amount': 1,
        'api_key': api_key
    }
    
    response = requests.get(url, params=params)
    
    if response.status_code == 200:
        data = response.json()
        # Check if 'response' contains the expected data
        if 'response' in data and 'value' in data['response']:
            exchange_rate = data['response']['value']  # Access the exchange rate here
            # Save the exchange rate
            save_exchange_rate(base_currency_code, target_currency_code, exchange_rate)
            return True

    return False
 
def save_exchange_rate(base_currency_code, target_currency_code, rate_value):
    try:
        base_currency = Currency.objects.get(code=base_currency_code)
        target_currency = Currency.objects.get(code=target_currency_code)
 
        exchange_rate = CurrencyExchangeRate.objects.create(
            source_currency=base_currency,
            exchanged_currency=target_currency,
            valuation_date=date.today(),  # Set valuation date to today
            rate_value=Decimal(rate_value)
        )
        return exchange_rate
    except ObjectDoesNotExist:
        print(f"Currency {base_currency_code} or {target_currency_code} not found.")
        return None

