from django import forms


class ChooseDeliveryForm(forms.Form):

    options = forms.ChoiceField(
        choices=[],
    )

    def __init__(self, *args, **kwargs):
        self.order = kwargs.pop('order')
        self.delivery_options = []
        super().__init__(*args, **kwargs)
        self.fields['options'].choices = self.delivery_options

    def add_delivery(self):
        raise NotImplementedError
