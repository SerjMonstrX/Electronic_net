from django.contrib import admin
from .models import Product


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('network_entity', 'creator', 'name', 'model', 'release_date')
    search_fields = ('name', 'model')
    list_filter = ('network_entity',)
