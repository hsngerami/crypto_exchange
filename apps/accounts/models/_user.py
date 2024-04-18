from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from django.dispatch import receiver

from apps.crypto_wallets.models import CryptoWallet, CryptoCurrency
from apps.wallets.models import Wallet


class User(AbstractUser):
    pass


@receiver(post_save, sender=User)
def create_user_related_objects(sender, instance, created, **kwargs):
    if created:
        Wallet.objects.create(owner=instance)
        CryptoWallet.objects.create(owner=instance, currency=CryptoCurrency.ABAN.value, price=4)