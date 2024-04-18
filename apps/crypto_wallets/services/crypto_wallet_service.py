from apps.crypto_wallets.models import CryptoWallet
from base.services import BaseService


class CryptoWalletService(BaseService):
    @classmethod
    def create_crypto_wallet(cls, user, currency):
        """
        Creates a crypto wallet for a user.

        :param user: The user to create the wallet for.
        :param currency: The currency of the wallet.
        :return: The crypto wallet.
        """
        return cls.create_instance(
            CryptoWallet,
            owner=user,
            currency=currency,
        )
