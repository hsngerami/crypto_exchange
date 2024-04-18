from drf_spectacular.utils import extend_schema
from rest_framework.permissions import IsAuthenticated
from rest_framework import mixins

from apps.orders.serializers.order import CreateOrderRequestSerializer, CreateOrderResponseSerializer
from apps.orders.services.order_service import OrderService
from base.api import BaseViewSet


class OrderViewSet(BaseViewSet, mixins.CreateModelMixin):
    permission_classes = [IsAuthenticated]
    serializer_class = CreateOrderRequestSerializer
    response_serializer_class = CreateOrderResponseSerializer

    @extend_schema(
        request=serializer_class,
        responses={
            201: response_serializer_class,
        },
    )
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        order = OrderService.create_order(
            user=request.user,
            **serializer.validated_data
        )
        order_data = {
            'id': order.id,
            'amount': order.amount,
            'currency': order.currency,
            'created_at': order.created_at,
            'updated_at': order.updated_at
        }
        return self.aban_response(order_data, status_code=201)
