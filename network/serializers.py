from rest_framework import serializers
from .models import NetworkEntity


class NetworkEntitySerializer(serializers.ModelSerializer):
    class Meta:
        model = NetworkEntity
        fields = '__all__'
        extra_kwargs = {
            'debt': {'read_only': True}  # Запрещаем обновление поля "debt" через API
        }
        read_only_fields = ['creator']
