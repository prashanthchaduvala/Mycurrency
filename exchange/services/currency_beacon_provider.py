import requests
from .provider_adapter import ExchangeRateProviderAdapter
 
class CurrencyBeaconProvider(ExchangeRateProviderAdapter):
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = 'https://api.currencybeacon.com/v1/'
        
    def get_exchange_rate_data(self, source_currency, exchanged_currency, valuation_date):
        endpoint = f"convert?from={source_currency}&to={exchanged_currency}&date={valuation_date}&api_key={self.api_key}"
        response = requests.get(f"{self.base_url}{endpoint}")
        data = response.json()

        if response.status_code == 200:
            return data['rate']
        return None