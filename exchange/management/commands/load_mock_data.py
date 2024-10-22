from django.core.management.base import BaseCommand
from exchange.models import CurrencyExchangeRate, Currency
from datetime import date, timedelta
import random
 
# class Command(BaseCommand):
#     help = 'Load mock historical data for testing'
 
#     def handle(self, *args, **kwargs):
#         currencies = Currency.objects.filter(code__in=['USD', 'EUR', 'GBP', 'CHF'])
#         start_date = date(2020, 1, 1)
#         end_date = date(2024, 10, 1)
 
#         current_date = start_date
#         while current_date <= end_date:
#             for source in currencies:
#                 for target in currencies:
#                     if source != target:
#                         CurrencyExchangeRate.objects.create(
#                             source_currency=source,
#                             exchanged_currency=target,
#                             valuation_date=current_date,
#                             rate_value=round(random.uniform(0.5, 2.0), 6)
#                         )
#             current_date += timedelta(days=1)
#         self.stdout.write(self.style.SUCCESS('Successfully loaded mock historical data'))

import requests
from django.core.management.base import BaseCommand
from exchange.models import *
 
class Command(BaseCommand):
    help = 'Fetch and store currency exchange rates from CurrencyBeacon'
 
    def handle(self, *args, **kwargs):
        # Define the API endpoint and your API key
        api_url = "https://api.currencybeacon.com/v1/currencies"
        api_key = "rgxHn8aJubkShWXs691HoqF26HdtYgxw"  # Replace with your actual API key
 
        # Set parameters (you can customize these based on the API documentation)
        params = {
            'api_key': api_key,
            'currency': 'EUR',  # Specify the currency you want to get rates for
            'base': 'USD',      # Specify the base currency
            # Add any other parameters as required
        }
 
        try:
            response = requests.get(api_url, params=params)
            response.raise_for_status()  # Raise an error for bad responses
 
            # Get the rates from the response
            data = response.json()
            
            currencies = data.get('response', {})
            
            # Iterate through currencies and store in the database
            for currencie in currencies:
                Currency.objects.update_or_create(
                    code=currencie['code'],
                    defaults={
                        'name': currencie['name'],
                        'code': currencie['short_code'],
                        'symbol': currencie['symbol'],
                    
                    }
                )
 
                # self.stdout.write(self.style.SUCCESS('Successfully fetched and stored currency rates.'))
        
        except requests.exceptions.RequestException as e:
            self.stderr.write(self.style.ERROR(f'Error fetching data: {e}'))

