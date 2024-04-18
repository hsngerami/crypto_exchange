from django.db import transaction, models

from apps.crypto_wallets.exceptions import LowCheckoutValueError
from apps.crypto_wallets.services.crypto_wallet_management_service import CryptoWalletManagementService
from apps.crypto_wallets.services.exchange_service import ExchangeService
from apps.orders.models import Order, OrderStatus, OrderType
from apps.wallets.services.wallet_management_service import WalletManagementService
from base.services import BaseService
from utils.constants import Constants


class OrderService(BaseService):

    @classmethod
    @transaction.atomic
    def create_order(cls, user, amount, currency, type) -> Order:
        order = cls.create_instance(
            Order,
            owner=user,
            amount=amount,
            currency=currency,
            type=type,
        )

        cls.checkout_order(order)

        return order

    @classmethod
    def checkout_order(cls, order):
        wallet = order.owner.wallet
        crypto_wallet = order.owner.crypto_wallet
        amount = order.amount
        currency = order.currency

        try:
            done = ExchangeService.checkout(currency, amount)
        except LowCheckoutValueError:
            order.status = OrderStatus.PENDING_CHECKOUT
            order.save()
            aggregate_result = (cls.get_queryset(Order)
                                .filter(status=OrderStatus.PENDING_CHECKOUT)
                                .aggregate(collected_orders_sum=models.Sum('amount')))
            if aggregate_result.get('collected_orders_sum') >= Constants.EXCHANGE_PROVIDER_MINIMUM_AMOUNT:
                done = ExchangeService.checkout(currency, aggregate_result.get('collected_orders_sum'))
            else:
                return

        if done is True:
            CryptoWalletManagementService.deposit(crypto_wallet, amount)
            WalletManagementService.withdraw(wallet, amount)
            order.status = OrderStatus.COMPLETED
            order.save()
