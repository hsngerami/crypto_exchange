from apps.crypto_wallets.models import CryptoTransactionType, CryptoWallet
from apps.crypto_wallets.services.crypto_wallet_transaction_service import CryptoWalletTransactionService
from base.services import BaseService


class CryptoWalletManagementService(BaseService):

    @classmethod
    def withdraw(cls, wallet, amount):
        crypto_amount = -amount / wallet.price
        CryptoWalletTransactionService.create_crypto_transaction(
            wallet,
            crypto_amount,
            CryptoTransactionType.WITHDRAWAL
        )

    @classmethod
    def deposit(cls, wallet: CryptoWallet, amount):
        crypto_amount = amount / wallet.price
        CryptoWalletTransactionService.create_crypto_transaction(
            wallet,
            crypto_amount,
            CryptoTransactionType.DEPOSIT
        )
