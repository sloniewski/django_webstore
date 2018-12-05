from django.contrib import admin

from .models import Order, OrderItem


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'uuid',
        'created',
        'value',
        'user',
    ]
    list_select_related = [
        'user'
    ]
    search_fields = ['user__email']

    def get_queryset(self, request):
        return self.model.objects.with_properties()


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = [
        'quantity',
        'price',
    ]
    list_select_related = [
        'product'
    ]
