from django.contrib import admin

from .models import Delivery, DeliveryPricing


@admin.register(Delivery)
class DeliveryAdmin(admin.ModelAdmin):
    pass


@admin.register(DeliveryPricing)
class DeliveryPricingAdmin(admin.ModelAdmin):
    pass
