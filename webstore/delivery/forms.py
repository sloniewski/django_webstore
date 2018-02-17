from django import forms

from webstore.delivery.models import DeliveryPricing


class ChooseDeliveryForm(forms.Form):

    options = forms.ModelChoiceField(
        queryset=[],
        required=True,
    )

    def __init__(self, order, *args, **kwargs):
        self.order = order
        delivery_options = []
        super().__init__(*args, **kwargs)
        self.fields['options'].queryset = delivery_options
