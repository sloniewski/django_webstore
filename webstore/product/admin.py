from django.contrib import admin
from django.utils.safestring import mark_safe

from . import models


def price(product):
    return product.get_price


@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):

    def product_image_tag(self, obj):
        return mark_safe('<img src="/{}" />'.format(
            obj.image_url
        ))

    product_image_tag.short_description = 'Image'
    readonly_fields = (
        'product_image_tag',
    )
    list_display = (
        'name',
        'category',
        'stock',
        price,
    )


@admin.register(models.Category)
class CategoryAdmin(admin.ModelAdmin):
    pass


@admin.register(models.Price)
class PriceAdmin(admin.ModelAdmin):
    list_display = (
        '__str__',
        'product',
        'valid_from',
    )


def location(obj):
    return obj.data.name


@admin.register(models.Picture)
class PictureAdmin(admin.ModelAdmin):

    def image_tag(self, obj):
        return mark_safe('<img src="/{}" />'.format(
            obj.data.url
        ))
    image_tag.short_description = 'Image'

    readonly_fields = ('image_tag',)
    list_display = [
        'name',
        location,
    ]


@admin.register(models.Gallery)
class GalleryAdmin(admin.ModelAdmin):
    pass