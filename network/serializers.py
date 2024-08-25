from rest_framework import serializers

from products.serializers import ProductSerializer
from .models import NetworkEntity


class NetworkEntitySerializer(serializers.ModelSerializer):
    """
    Сериализатор для объекта сети.
    """
    products = ProductSerializer(many=True, read_only=True)

    class Meta:
        model = NetworkEntity
        fields = '__all__'
        read_only_fields = ['creator', 'debt']
