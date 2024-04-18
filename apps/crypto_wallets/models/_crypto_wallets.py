from django.db import models

from base.models import BaseModel


class CryptoCurrency(models.TextChoices):
    USDT = 'usdt'
    BTC = 'btc'
    ABAN = 'aban'


class CryptoWallet(BaseModel):
    owner = models.OneToOneField('accounts.User', on_delete=models.CASCADE, related_name='crypto_wallet')

    currency = models.CharField(max_length=10, choices=CryptoCurrency.choices)
    # every currency has a price in USD
    price = models.BigIntegerField()

    @property
    def balance(self):
        return self.transactions.aggregate(balance=models.Sum('amount')).get('balance', 0)
