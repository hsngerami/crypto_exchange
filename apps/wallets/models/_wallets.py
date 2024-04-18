from django.db import models

from base.models import BaseModel


class Wallet(BaseModel):
    owner = models.OneToOneField('accounts.User', on_delete=models.CASCADE, related_name='wallet')

    @property
    def balance(self):
        return self.transactions.aggregate(balance=models.Sum('amount')).get('balance', 0)
