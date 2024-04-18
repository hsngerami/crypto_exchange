from django.urls import reverse

from apps.crypto_wallets.models import CryptoCurrency, CryptoWalletTransaction
from apps.orders.models import OrderType
from apps.orders.tests.fixtures.user_fixture import UserFixture
from apps.wallets.models import WalletTransaction, TransactionType
from base.tests import BaseTestCase


class CreateOrderTestCase(BaseTestCase):
    order_url = reverse('orders-list')

    def test_create_order(self):
        """
        Test submit an order to buy 12$ ABAN CryptoCurrency
        """

        self.user = UserFixture()
        self.auth(username=self.user.username, password=UserFixture.raw_password())

        dollar_amount = 12

        response = self.client.post(self.order_url, {
            'type': OrderType.BUY.value,
            'amount': dollar_amount,
            'currency': CryptoCurrency.ABAN.value,
        })
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json()['data']['amount'], dollar_amount)
        self.assertEqual(response.json()['data']['currency'], CryptoCurrency.ABAN.value)

        transaction = WalletTransaction.objects.get(wallet=self.user.wallet)

        self.assertEqual(transaction.amount, dollar_amount)
        self.assertEqual(transaction.transaction_type, TransactionType.WITHDRAWAL.value)

        crypto_transaction = CryptoWalletTransaction.objects.get(wallet__owner=self.user)
        self.assertEqual(crypto_transaction.amount, dollar_amount / self.user.crypto_wallet.price)
        self.assertEqual(crypto_transaction.transaction_type, TransactionType.DEPOSIT.value)
