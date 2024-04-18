from apps.crypto_wallets.models import CryptoWalletTransaction
from base.services import BaseService


class CryptoWalletTransactionService(BaseService):

    @classmethod
    def create_crypto_transaction(cls, wallet, amount, transaction_type):
        """
        Creates a crypto wallet transaction.

        :param wallet: The wallet to create the transaction for.
        :param amount: The amount of the transaction.
        :param transaction_type: The type of the transaction.
        :return: The crypto wallet transaction.
        """
        return cls.create_instance(
            CryptoWalletTransaction,
            wallet=wallet,
            amount=amount,
            transaction_type=transaction_type,
        )
