from rest_framework import serializers

from base.serializers import BaseResponseSerializer


class BaseIdentifierSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=255, required=True)

class LoginRequestSerializer(BaseIdentifierSerializer):
    password = serializers.CharField(required=True, write_only=True)


class LoginDataResponseSerializer(serializers.Serializer):
    access = serializers.CharField(required=False)
    refresh = serializers.CharField(required=False)
    user = serializers.JSONField(required=False)
    message = serializers.CharField(required=False)


class LoginResponseSerializer(BaseResponseSerializer):
    data = LoginDataResponseSerializer()


class RefreshTokenRequestSerializer(serializers.Serializer):
    refresh = serializers.CharField(required=True)
