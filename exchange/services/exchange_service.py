from .currency_beacon_provider import CurrencyBeaconProvider
from .mock_provider import MockProvider
from exchange.models import *
# class ExchangeRateService:
#     def __init__(self):
#         self.providers = [
#             {"provider": CurrencyBeaconProvider(api_key="your_api_key"), "priority": 1, "active": True},
#             {"provider": MockProvider(), "priority": 2, "active": True}
#         ]
    
#     def get_exchange_rate(self, source_currency, exchanged_currency, valuation_date):
#         for provider_data in sorted(self.providers, key=lambda p: p['priority']):
#             if provider_data['active']:
#                 rate = provider_data['provider'].get_exchange_rate_data(source_currency, exchanged_currency, valuation_date)
#                 if rate:
#                     return rate
#         return None

class ExchangeRateService:
    def __init__(self):
        self.providers = self.get_active_providers()
 
    def get_active_providers(self):
        # Fetch active providers ordered by priority
        return Provider.objects.filter(active=True).order_by('priority')
 
    def get_exchange_rate(self, source_currency, exchanged_currency, valuation_date):
        for provider_data in self.providers:
            provider_instance = self.get_provider_instance(provider_data.name)
            if provider_instance:
                rate = provider_instance.get_exchange_rate_data(source_currency, exchanged_currency, valuation_date)
                if rate:
                    return rate
        return None

    def get_provider_instance(self, provider_name):
        # Return provider instance based on name
        if provider_name == "CurrencyBeacon":
            return CurrencyBeaconProvider(api_key="rgxHn8aJubkShWXs691HoqF26HdtYgxw") # my api key
        elif provider_name == "Mock":
            return MockProvider()
        return None
