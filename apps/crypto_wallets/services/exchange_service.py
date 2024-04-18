from apps.crypto_wallets.exceptions import LowCheckoutValueError
from base.clients.exchange_client import ExchangeClient
from base.services import BaseService
from utils.constants import Constants


class ExchangeService(BaseService):
    @classmethod
    def checkout(cls, currency, amount):
        """
        Checkout funds from an exchange.

        :param currency: The currency to checkout.
        :param amount: The amount to checkout.
        :return:
        """
        exchange_client = ExchangeClient("example_base_url")

        if amount < Constants.EXCHANGE_PROVIDER_MINIMUM_AMOUNT:
            raise LowCheckoutValueError(f"Amount must be greater than {Constants.EXCHANGE_PROVIDER_MINIMUM_AMOUNT}")

        is_success = exchange_client.buy_from_exchange(amount, currency)
        return is_success
