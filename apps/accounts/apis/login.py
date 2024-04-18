import logging

from drf_standardized_errors.openapi_serializers import Error401Serializer
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView
from drf_spectacular.utils import extend_schema
from apps.accounts.serializers.jwt_token import LoginRequestSerializer, LoginDataResponseSerializer, \
    LoginResponseSerializer, RefreshTokenRequestSerializer
from apps.accounts.services.auth_service import AuthService
from base.api import BaseAPIView

logger = logging.getLogger(__name__)


class LoginAPI(BaseAPIView):
    serializer_class = LoginRequestSerializer
    response_serializer_class = LoginResponseSerializer
    permission_classes = [AllowAny]

    @extend_schema(
        request=serializer_class,
        responses={
            200: response_serializer_class,
            401: Error401Serializer,
        },
    )
    def post(self, request, *args, **kwargs):
        req_serializer = self.serializer_class(data=request.data)
        req_serializer.is_valid(raise_exception=True)
        user_auth_data = AuthService.authenticate_user(**req_serializer.validated_data)
        return self.aban_response(user_auth_data)


class RefreshToken(BaseAPIView):
    serializer_class = RefreshTokenRequestSerializer
    response_serializer_class = LoginResponseSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        req_serializer = self.serializer_class(data=request.data)
        req_serializer.is_valid(raise_exception=True)
        user_auth_data = AuthService.refresh_token(refresh_token=req_serializer.validated_data['refresh'])
        return self.aban_response(user_auth_data)
