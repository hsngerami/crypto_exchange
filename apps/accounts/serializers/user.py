from rest_framework import serializers

from apps.accounts.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ('id', 'password', 'is_superuser', 'is_staff',
                   'groups', 'user_permissions', 'is_active', 'last_login', 'date_joined')
