from django import forms

from webstore.order.models import Order
from webstore.core.widgets import MaterializeCheckboxInput


class OrderUpdateForm(forms.ModelForm):
    send_mail = forms.BooleanField(
        widget=MaterializeCheckboxInput(),
        help_text='Send email to client with information about status change',
    )

    class Meta:
        model = Order
        fields = [
            'status'
        ]
