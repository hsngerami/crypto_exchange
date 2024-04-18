import os


class ThrottleScope:
    # app level scopes
    Default = "default"
    Accounts = "accounts"
    Wallets = "wallets"

    scopes = {
        Default: '100/minute',
        Accounts: '100/minute',
        Wallets: '100/minute',
    }

    @classmethod
    def as_env(cls):
        return ",".join([f"{key}={value}" for key, value in cls.scopes.items()])

    @staticmethod
    def as_settings_from_env(env_value):
        scopes = env_value.split(',')
        return {scope.split('=')[0]: scope.split('=')[1] for scope in scopes}


class Constants:
    THROTTLE_RATE = os.getenv('THROTTLE_RATE', ThrottleScope.as_env())

    EXCHANGE_PROVIDER_MINIMUM_AMOUNT = 12  # Minimum amount to deposit or withdraw from the exchange provider.
