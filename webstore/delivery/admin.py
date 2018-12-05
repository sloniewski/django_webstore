from django.contrib import admin

from .models import Delivery, DeliveryPricing


@admin.register(Delivery)
class DeliveryAdmin(admin.ModelAdmin):
    list_display = [
        'name',
        'surname',
        'city',
        'country',
        'postal_code',
        'street_name',
        'street_number',
        'cost',
    ]
    readonly_fields = [
        'created',
        'modified',
        'order',
    ]


@admin.register(DeliveryPricing)
class DeliveryPricingAdmin(admin.ModelAdmin):
    list_display = [
        'name',
        'cost',
    ]
