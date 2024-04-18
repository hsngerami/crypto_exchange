import factory
from django.contrib.auth.hashers import make_password


class UserFixture(factory.django.DjangoModelFactory):
    class Meta:
        model = 'accounts.User'

    @staticmethod
    def raw_password():
        return 'password'

    first_name = 'hossein'
    last_name = 'gerami'
    username = factory.Sequence(lambda n: f'user{n}')
    email = factory.Sequence(lambda n: f'user{n}@example.com')
    password = make_password(raw_password())
