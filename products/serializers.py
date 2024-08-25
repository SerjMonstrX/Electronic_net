from rest_framework import serializers
from .models import Product


class ProductSerializer(serializers.ModelSerializer):
    """
    Сериализатор для продукта.
    """
    class Meta:
        model = Product
        fields = ['id', 'name', 'model', 'release_date', 'creator', 'network_entity']
        read_only_fields = ['creator']

    def update(self, instance, validated_data):
        # Используем старые значения, если новые не переданы
        instance.name = validated_data.get('name', instance.name)
        instance.model = validated_data.get('model', instance.model)
        instance.release_date = validated_data.get('release_date', instance.release_date)
        instance.network_entity = validated_data.get('network_entity', instance.network_entity)

        # Сохраняем обновленный объект
        instance.save()
        return instance

    def validate(self, data):
        network_entity = data.get('network_entity')
        if network_entity.supplier_type == 0:  # Завод
            return data
        elif Product.objects.filter(
                network_entity=network_entity.supplier,
                name=data.get('name'),
                model=data.get('model')
        ).exists():
            return data
        else:
            raise serializers.ValidationError(
                "Продукт должен существовать у поставщика."
            )
