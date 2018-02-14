from django import forms

from webstore.delivery.managers import DeliveryManager


class ChooseDeliveryForm(forms.Form):

    options = forms.ModelChoiceField(
        queryset=[],
    )

    def __init__(self, order=None, *args, **kwargs):
        self.order = order
        delivery_manager = DeliveryManager()
        delivery_options = delivery_manager.get_form_choices(self.order)
        super().__init__(*args, **kwargs)
        self.fields['options'].queryset = delivery_options

    def save(self):
        raise NotImplementedError('this method was not implemented')
