from django.core.management import BaseCommand

from apps.accounts.models import User
from apps.orders.tests.fixtures.user_fixture import UserFixture


class Command(BaseCommand):
    help = "Setup default user"

    def handle(self, *args, **options):
        if User.objects.filter(username='user0').exists():
            return
        UserFixture()
