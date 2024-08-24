from rest_framework import serializers
from .models import NetworkEntity


class NetworkEntitySerializer(serializers.ModelSerializer):
    """
    Сериализатор для объекта сети.
    """
    class Meta:
        model = NetworkEntity
        fields = '__all__'
        read_only_fields = ['creator', 'debt']
