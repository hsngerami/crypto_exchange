from apps.wallets.models import WalletTransaction
from base.services import BaseService


class WalletTransactionService(BaseService):

    @classmethod
    def create_transaction(cls, wallet, amount, transaction_type):
        """
        Creates a wallet transaction.

        :param wallet: The wallet to create the transaction for.
        :param amount: The amount of the transaction.
        :param transaction_type: The type of the transaction.
        :return: The wallet transaction.
        """
        return cls.create_instance(
            WalletTransaction,
            wallet=wallet,
            amount=amount,
            transaction_type=transaction_type,
        )
