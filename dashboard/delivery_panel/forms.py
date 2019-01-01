from django import forms

import django_filters

from webstore.delivery.models import Delivery, DeliveryPricing
from webstore.core.widgets import MaterializeCheckboxInput


class FilterDeliveriesForm(django_filters.FilterSet):
    name = django_filters.CharFilter(
        field_name='name',
        lookup_expr='icontains',
    )
    surname = django_filters.CharFilter(
        field_name='surname',
        lookup_expr='icontains',
    )
    city = django_filters.CharFilter(
        field_name='city',
        lookup_expr='icontains',
    )
    street = django_filters.CharFilter(
        field_name='street',
        lookup_expr='icontains',
    )

    class Meta:
        model = Delivery
        fields = [
            'name',
            'surname',
            'city',
            'street',
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
