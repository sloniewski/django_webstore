from django import forms

from webstore.payment.models import Payment


class ChoosePaymentForm(forms.ModelForm):

    def __init__(self, order, *args, **kwargs):
        self.order = order
        super().__init__(*args, **kwargs)

    def save(self, *args, **kwargs):
        self.instance.order = self.order
        return super().save()

    
    class Meta:
        model = Payment
        fields = [
            'method',
        ]
