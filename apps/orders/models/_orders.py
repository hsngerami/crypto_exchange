from django.db import models

from apps.crypto_wallets.models import CryptoCurrency
from base.models import BaseModel

class OrderType(models.TextChoices):
    BUY = 'buy'
    SELL = 'sell'

class OrderStatus(models.TextChoices):
    PENDING = 'pending'
    PENDING_CHECKOUT = 'pending_checkout'
    COMPLETED = 'completed'
    CANCELLED = 'cancelled'
    FAILED = 'failed'

class Order(BaseModel):
    owner = models.ForeignKey('accounts.User', on_delete=models.CASCADE)
    amount = models.BigIntegerField()
    currency = models.CharField(max_length=10, choices=CryptoCurrency.choices)
    status = models.CharField(max_length=20, choices=OrderStatus.choices, default=OrderStatus.PENDING)
    type = models.CharField(max_length=10, choices=OrderType.choices)
