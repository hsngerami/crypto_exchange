from django.db import models

from base.models import BaseModel


class CryptoTransactionType(models.TextChoices):
    DEPOSIT = 'deposit'
    WITHDRAWAL = 'withdrawal'


class CryptoWalletTransaction(BaseModel):
    wallet = models.ForeignKey('crypto_wallets.CryptoWallet', on_delete=models.CASCADE, related_name='transactions')
    transaction_type = models.CharField(max_length=10)
    amount = models.DecimalField(max_digits=20, decimal_places=5)
