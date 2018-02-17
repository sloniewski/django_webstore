from django import forms

from webstore.delivery.models import DeliveryPricing, Delivery, DeliveryOption


class ChooseDeliveryForm(forms.Form):
    delimiter = '-'

    option = forms.ChoiceField(
        choices=[],
    )

    def __init__(self, order, *args, **kwargs):
        self.order = order
        prices = DeliveryPricing.objects.get_prices_for_order(order)
        delivery_options = [x.form_choice(self.delimiter) for x in prices]
        super().__init__(*args, **kwargs)
        self.fields['option'].choices = delivery_options

    def add_delivery(self):
        delivery_option_name, price_string = self.cleaned_data['option'].split(self.delimiter)
        delivery_option = DeliveryOption.objects.get(name=delivery_option_name)
        price, currency = price_string.split(' ')
        delivery = Delivery.objects.create(
            order=self.order,
            delivery_option=delivery_option,
            price=price,
        )
        return delivery
