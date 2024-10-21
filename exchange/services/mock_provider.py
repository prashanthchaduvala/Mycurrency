import random
from datetime import datetime
from .provider_adapter import ExchangeRateProviderAdapter


class MockProvider(ExchangeRateProviderAdapter):
    def get_exchange_rate_data(self, source_currency, exchanged_currency, valuation_date):
        # Return random mock rates for demonstration
        random.seed(datetime.now())
        return round(random.uniform(0.5, 2.0), 6)