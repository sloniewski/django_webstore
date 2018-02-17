from django import forms

from webstore.delivery.models import DeliveryPricing


class ChooseDeliveryForm(forms.Form):

    options = forms.ChoiceField(
        choices=[],
    )

    def __init__(self, order, *args, **kwargs):
        self.order = order
        prices = DeliveryPricing.objects.get_prices_for_order(order)
        delivery_options = [x.form_choice for x in prices]
        super().__init__(*args, **kwargs)
        self.fields['options'].choices = delivery_options
