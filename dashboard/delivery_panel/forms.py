from django import forms

import django_filters

from webstore.delivery.models import Delivery, DeliveryStatus
from webstore.order.models import Order, OrderStatus


class FilterDelieriesForm(django_filters.FilterSet):

    class Meta:
            model = Delivery
            fields = '__all__'


class DeliveryUpdateForm(forms.ModelForm):

    status = forms.ChoiceField(
        choices=DeliveryStatus.choices(),
    )

    def save(self, commit=True):
        object = super().save(commit)

        if object.status == DeliveryStatus.SHIPPED.name:
            order = object.order
            order.status = OrderStatus.CLOSED.name
            order.save()

        return object

    class Meta:
        model = Delivery
        fields = [
            'status',
        ]
