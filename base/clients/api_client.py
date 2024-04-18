import logging

import requests

logger = logging.getLogger(__name__)

class APIClient:
    def __init__(self, base_url: str, **kwargs):
        self.base_url = base_url

    def _get_auth_headers(self):
        raise NotImplementedError()

    def make_request(self, method, endpoint, **kwargs):
        raise_exception = kwargs.pop('raise_exception', True)
        if 'headers' not in kwargs:
            kwargs['headers'] = self._get_auth_headers()
        url = self.base_url + endpoint
        logger.info(f'Making request to url: {url}, method: {method}, kwargs: {kwargs}')
        response = requests.request(method, url, **kwargs)
        if raise_exception:
            response.raise_for_status()
        return response
