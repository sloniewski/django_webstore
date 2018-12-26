from django import forms

from webstore.order.models import Order, OrderItem
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


class OrderEditForm(forms.ModelForm):

    class Meta:
        model = OrderItem
        fields = [
            'product',
            'quantity',
            'price',
        ]


item_formset = forms.inlineformset_factory(
                        model=OrderItem,
                        parent_model=Order,
                        form=OrderEditForm,
                        extra=2,
                )

