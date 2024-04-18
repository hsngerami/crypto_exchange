import logging

from django.urls import reverse
from rest_framework.test import APITestCase

logger = logging.getLogger(__name__)

class BaseTestCase(APITestCase):

    def _login(self, username, password):
        login_url = reverse('login')
        response = self.client.post(login_url, {
            'username': username,
            'password': password,
        })
        return response.json()['data']['access'], response.json()['data']['refresh']

    def auth(self, username, password):
        access_token, _ = self._login(
            username=username,
            password=password
        )
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')
