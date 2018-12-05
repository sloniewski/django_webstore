from django import forms

import django_filters

from webstore.delivery.models import Delivery
from webstore.order.models import OrderStatus


class FilterDelieriesForm(django_filters.FilterSet):

    class Meta:
            model = Delivery
            fields = '__all__'


class DeliveryUpdateForm(forms.ModelForm):

    status = forms.ChoiceField(
        choices=OrderStatus.choices(),
    )

    class Meta:
        model = Delivery
        fields = [
            'status',
        ]
