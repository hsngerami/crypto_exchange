import logging
from random import randint

from django.contrib.auth.hashers import make_password
from django.core.exceptions import ValidationError
from rest_framework.exceptions import AuthenticationFailed, ValidationError as DRFValidationError
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer, TokenRefreshSerializer

from apps.accounts.models import User
from apps.accounts.serializers.user import UserSerializer
from apps.accounts.services.user_service import UserService
from base.services import BaseService

logger = logging.getLogger(__name__)


class AuthService(BaseService):
    """
    Service class for handling authentication-related operations.
    """

    OTP_KEY_PREFIX = "otp"

    @classmethod
    def create_jwt_token_by_user(cls, user):
        """
        Creates a JWT token for the provided user.
        """
        token = TokenObtainPairSerializer.get_token(user)
        return {
            'refresh': str(token),
            'access': str(token.access_token),
        }

    @classmethod
    def authenticate_user(cls, username, password):
        """
        Authenticates the user with the provided destination address and password.
        """
        try:
            user = UserService.get_user_by_username(username)
        except User.DoesNotExist:
            logger.error(f"user with {username} does not exist.")
            raise AuthenticationFailed()
        if user.check_password(password) is False:
            logger.error(f"Authentication failed for {username}.")
            raise AuthenticationFailed()
        token_data = cls.create_jwt_token_by_user(user)
        logger.info(f"User {user.username} authenticated successfully.")
        user_data = {
            **token_data,
            'username': username,
            'user': UserSerializer(user).data
        }
        return user_data

    @classmethod
    def refresh_token(cls, refresh_token):
        """
        Refreshes the access token with the provided refresh token.
        """
        auth_data = TokenRefreshSerializer().validate({'refresh': refresh_token})
        return auth_data
