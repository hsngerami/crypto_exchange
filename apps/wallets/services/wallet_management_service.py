from apps.wallets.models import TransactionType
from apps.wallets.services.wallet_transaction_service import WalletTransactionService
from base.services import BaseService


class WalletManagementService(BaseService):

    @classmethod
    def deposit(cls, wallet, amount):
        """
        Deposits funds into a wallet.

        :param wallet: The wallet to deposit funds into.
        :param amount: The amount to deposit.
        :return: The wallet transaction.
        """
        return WalletTransactionService.create_transaction(wallet, amount, TransactionType.DEPOSIT)

    @classmethod
    def withdraw(cls, wallet, amount):
        """
        Withdraws funds from a wallet.

        :param wallet: The wallet to withdraw funds from.
        :param amount: The amount to withdraw.
        :return: The wallet transaction.
        """
        instance = WalletTransactionService.create_transaction(wallet, amount, TransactionType.WITHDRAWAL)
