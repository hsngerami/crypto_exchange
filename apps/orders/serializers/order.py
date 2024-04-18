from rest_framework import serializers

from apps.orders.models import Order


class CreateOrderRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['amount', 'currency', 'type']


class CreateOrderDataResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['id', 'amount', 'currency', 'created_at', 'updated_at']


class CreateOrderResponseSerializer(serializers.Serializer):
    data = CreateOrderDataResponseSerializer()