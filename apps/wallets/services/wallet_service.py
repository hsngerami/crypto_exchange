from apps.wallets.models import Wallet
from base.services import BaseService


class WalletService(BaseService):

    @classmethod
    def create_wallet(cls, self, owner):
        return cls.create_instance(Wallet, owner=owner)