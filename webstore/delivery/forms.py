from django import forms


class ChooseDeliveryForm(forms.Form):

    options = forms.ChoiceField(
        choices=[],
    )

    def __init__(self, order, *args, **kwargs):
        self.delivery_options = []
        super().__init__(*args, **kwargs)
        self.fields['options'].choices = self.delivery_options

