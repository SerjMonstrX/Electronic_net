from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from products.models import Product
from .models import NetworkEntity


class ProductInline(admin.TabularInline):
    model = Product
    extra = 1


@admin.action(description='Очистить задолженность перед поставщиком')
def clear_supplier_debt(self, request, queryset):
    updated_count = queryset.update(debt=0)
    self.message_user(request, f'Задолженность перед поставщиком очищена для {updated_count} объектов.')


@admin.register(NetworkEntity)
class NetworkEntityAdmin(admin.ModelAdmin):
    list_display = (
        'name', 'creator', 'email', 'country', 'city', 'street', 'building_number', 'supplier_link', 'debt', 'created_at', 'level')
    list_filter = ('city',)
    search_fields = ('name', 'city', 'country', 'creator',)
    readonly_fields = ('created_at',)
    inlines = [ProductInline]
    actions = [clear_supplier_debt]

    # Метод для отображения поставщика как ссылки
    def supplier_link(self, obj):
        if obj.supplier:
            url = reverse('admin:network_networkentity_change', args=[obj.supplier.pk])
            return format_html('<a href="{}">{}</a>', url, obj.supplier.name)
        return "Нет поставщика"

    supplier_link.short_description = 'Поставщик'
