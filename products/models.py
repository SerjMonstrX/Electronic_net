from django.db import models
from network.models import NetworkEntity
from django.contrib.auth import get_user_model


User = get_user_model()

NULLABLE = {'blank': True, 'null': True}


class Product(models.Model):
    creator = models.ForeignKey(User, on_delete=models.PROTECT, verbose_name='создатель')
    network_entity = models.ForeignKey(NetworkEntity, on_delete=models.CASCADE, related_name='products')
    name = models.CharField(max_length=255, verbose_name='название продукта')
    model = models.CharField(max_length=255, verbose_name='модель продукта', **NULLABLE)
    description = models.TextField(verbose_name='описание продукта', **NULLABLE)
    release_date = models.DateField(verbose_name='дата выхода на рынок', **NULLABLE)

    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'

    def __str__(self):
        return f"{self.name} ({self.model})"
