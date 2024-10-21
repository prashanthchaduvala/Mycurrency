from django.db import models

# Create your models here.
class Currency(models.Model):
    code = models.CharField(max_length=3, unique=True)
    name = models.CharField(max_length=20, db_index=True)
    symbol = models.CharField(max_length=10)
 
    def __str__(self):
        return self.code
 
class CurrencyExchangeRate(models.Model):
    source_currency = models.ForeignKey(Currency, related_name='exchanges', on_delete=models.CASCADE)
    exchanged_currency = models.ForeignKey(Currency, on_delete=models.CASCADE)
    valuation_date = models.DateField(db_index=True)
    rate_value = models.DecimalField(decimal_places=6, max_digits=18)
 
    def __str__(self):
        return f"{self.source_currency} to {self.exchanged_currency} on {self.valuation_date}"
    

class Provider(models.Model):
    name = models.CharField(max_length=100)
    priority = models.IntegerField(default=1)
    active = models.BooleanField(default=True)
 
    def __str__(self):
        return self.name