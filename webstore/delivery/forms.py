from django import forms

from webstore.delivery.models import Delivery, DeliveryPricing


class ChooseDeliveryForm(forms.ModelForm):

    cost = forms.ChoiceField(
        choices=[],
        widget=forms.Select(attrs={'class': 'browser-default'})
    )

    def __init__(self, cart, *args, **kwargs):
        delivery_options = DeliveryPricing.objects.get_prices_for_cart(cart)
        super().__init__(*args, **kwargs)
        self.fields['cost'].choices = delivery_options

    class Meta:
        model = Delivery
        fields = [
            'name',
            'surname',
            'street_name',
            'street_number',
            'flat_number',
            'city',
            'country',
            'postal_code',
            'cost',
        ]
