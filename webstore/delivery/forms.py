from django import forms

from webstore.delivery.managers import DeliveryManager


class ChooseDeliveryForm(forms.Form):

    options = forms.ChoiceField(
        choices=[],
    )

    def __init__(self, *args, **kwargs):
        self.order = kwargs.pop('order')
        delivery_manager = DeliveryManager()
        self.delivery_options = delivery_manager.get_form_choices(self.order)
        super().__init__(*args, **kwargs)
        self.fields['options'].choices = self.delivery_options

    def add_delivery(self):
        raise NotImplementedError('this method was not implemented')
