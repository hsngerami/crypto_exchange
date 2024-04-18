from django.db import models

from base.models import BaseModel


class TransactionType(models.TextChoices):
    DEPOSIT = 'deposit'
    WITHDRAWAL = 'withdrawal'


class WalletTransaction(BaseModel):
    wallet = models.ForeignKey('wallets.Wallet', related_name='transactions', on_delete=models.CASCADE)
    transaction_type = models.CharField(max_length=10, choices=TransactionType.choices)
    amount = models.BigIntegerField()
