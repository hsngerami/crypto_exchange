import logging

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet

from base.serializers import BaseListResponseSerializer
from utils.constants import ThrottleScope

logger = logging.getLogger(__name__)


class ABANMixin:
    permission_classes = None
    response_serializer_class = None
    throttle_scope = ThrottleScope.Default

    def get_authenticators(self):
        if AllowAny in self.permission_classes or AllowAny in self.permission_classes:
            return []
        return super().get_authenticators()

    def aban_response(self, data: dict, status_code=status.HTTP_200_OK):
        response_serializer = self.get_response_serializer_class()
        if response_serializer is None:
            return Response(data, status=status_code)
        is_list = issubclass(response_serializer, BaseListResponseSerializer)
        if is_list:
            return Response(
                response_serializer(data).data,
                status=status_code
            )
        response_data = {'data': data}
        serializer_instance = response_serializer(data=response_data)
        serializer_instance.is_valid(raise_exception=True)
        return Response(
            response_data,
            status=status_code
        )

    def get_response_serializer_class(self):
        return self.response_serializer_class


class BaseViewSet(ABANMixin, GenericViewSet):
    http_method_names = ['get', 'post', 'put', 'patch', 'delete']
    filter_backends = (DjangoFilterBackend,)


class BaseAPIView(ABANMixin, APIView):
    pass
