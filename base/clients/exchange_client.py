from base.clients.api_client import APIClient


class ExchangeClient(APIClient):
    def buy_from_exchange(self, amount, currency):
        """
        Buy amount of currency from exchange
        """
        # return self.make_request('POST', '/buy', json={'amount': amount, 'currency': currency})
        is_success = True
        return is_success
