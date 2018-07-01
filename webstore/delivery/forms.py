from django import forms

from webstore.delivery.models import Delivery, DeliveryPricing


class ChooseDeliveryForm(forms.ModelForm):

    price = forms.ChoiceField(
        choices=[],
        widget=forms.Select(attrs={'class': 'browser-default'})
    )

    def __init__(self, cart, *args, **kwargs):
        delivery_options = DeliveryPricing.objects.get_prices_for_cart(cart)
        super().__init__(*args, **kwargs)
        self.fields['price'].choices = delivery_options

    class Meta:
        model = Delivery
        fields = ['name', 'surname', 'street_name', 'street_number', 'flat_number', 'price']
