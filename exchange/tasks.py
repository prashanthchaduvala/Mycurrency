from celery import shared_task
from .services.exchange_service import ExchangeRateService
 
@shared_task
def load_historical_data(start_date, end_date):
    # Load data for all active currencies for the given date range
    service = ExchangeRateService()
    print(service,'11111111111111111111111111111')
    # Example of how you might loop through dates and retrieve data
    for date in date_range(start_date, end_date):
        for currency in ['EUR', 'USD', 'GBP', 'CHF']:
            for target_currency in ['EUR', 'USD', 'GBP', 'CHF']:
                if currency != target_currency:
                    service.get_exchange_rate(currency, target_currency, date)