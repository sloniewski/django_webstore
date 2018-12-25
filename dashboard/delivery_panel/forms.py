from django import forms

import django_filters

from webstore.delivery.models import Delivery, DeliveryPricing
from webstore.core.widgets import MaterializeCheckboxInput


class FilterDeliveriesForm(django_filters.FilterSet):

    class Meta:
        model = Delivery
        fields = [
            'name',
            'surname',
            'city',
        ]


class DeliveryUpdateForm(forms.ModelForm):

    class Meta:
        model = Delivery
        fields = [
            'name',
            'surname',
            'street_name',
            'street_number',
            'flat_number',
            'city',
            'postal_code',
            'cost',
        ]


class DeliveryPricingForm(forms.ModelForm):
    active = forms.BooleanField(
        widget=MaterializeCheckboxInput(),
    )

    class Meta:
        model = DeliveryPricing
        fields = [
            'name',
            'cost',
            'max_weight',
            'active',
        ]
