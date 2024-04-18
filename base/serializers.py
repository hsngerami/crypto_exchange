from rest_framework import serializers


class BaseResponseSerializer(serializers.Serializer):
    data = serializers.DictField(required=True)


class BaseListResponseSerializer(serializers.Serializer):
    count = serializers.IntegerField(required=True)
    next = serializers.URLField(required=False)
    previous = serializers.URLField(required=False)
    results = None
