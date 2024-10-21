 
class ExchangeRateProviderAdapter:
    def get_exchange_rate_data(self, source_currency, exchanged_currency, valuation_date):
        raise NotImplementedError("Subclasses must implement this method")