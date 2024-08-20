from django.db import models
from django.urls import reverse
from django.contrib.auth import get_user_model


User = get_user_model()
NULLABLE = {'blank': True, 'null': True}


class NetworkEntity(models.Model):

    TYPE_CHOICES = (
        (0, 'завод'),
        (1, 'розничная сеть'),
        (2, 'индивидуальный предприниматель'),
    )

    creator = models.ForeignKey(User, on_delete=models.PROTECT, verbose_name='создатель')
    name = models.CharField(max_length=255, verbose_name='название')
    email = models.EmailField(verbose_name='email')
    country = models.CharField(max_length=100, verbose_name='страна')
    city = models.CharField(max_length=100, verbose_name='город', **NULLABLE)
    street = models.CharField(max_length=100, verbose_name='улица', **NULLABLE)
    building_number = models.CharField(max_length=10, verbose_name='номер дома', **NULLABLE)
    supplier = models.ForeignKey('self', on_delete=models.SET_NULL, verbose_name='Поставщик',
                                 related_name='clients', **NULLABLE)
    debt = models.DecimalField(max_digits=12, decimal_places=2, default=0.00,
                               verbose_name='Задолженность перед поставщиком', **NULLABLE)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Время создания')
    supplier_type = models.IntegerField(choices=TYPE_CHOICES, default=0, verbose_name='тип поставщика')
    level = models.PositiveIntegerField(editable=False, verbose_name='уровень иерархии')

    class Meta:
        verbose_name = 'Объект сети'
        verbose_name_plural = 'Объекты сети'

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        """При сохранении поставщиков автоматически определяется уровень иерархии"""
        if self.supplier_type == 0:
            self.supplier = None  # У завода не должно быть поставщика
            self.level = 0
        elif self.supplier:  # Устанавливаем на один уровень ниже уровня поставщика
            self.level = self.supplier.level + 1
        else:
            self.level = 1  # Указываем уровень по умолчанию для новых объектов, если поставщик не задан

        super().save(*args, **kwargs)

    def get_admin_url(self):
        return reverse("admin:network_networkentity_change", args=[self.pk])
