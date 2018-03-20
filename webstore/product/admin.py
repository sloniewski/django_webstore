from django.contrib import admin

from .models import Product, Category, Price


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'category',
        'stock',
        'price',
    )


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    pass


@admin.register(Price)
class PriceAdmin(admin.ModelAdmin):
    list_display = (
        '__str__',
        'product',
        'valid_from',
    )
