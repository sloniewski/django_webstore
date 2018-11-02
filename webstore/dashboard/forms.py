from django import forms
from django.core.mail import send_mail

from webstore.core.forms import FilterForm
from webstore.core.widgets import MaterializeCheckboxInput
from webstore.order.models import OrderStatus
from webstore.payment.models import Payment, PaymentStatus
from webstore.delivery.models import Delivery, DeliveryStatus
from webstore.product.models import Product


class AddProductForm(forms.ModelForm):
    active = forms.BooleanField(
        widget=MaterializeCheckboxInput(),
    )

    class Meta:
        model = Product
        fields = [
            'name',
            'active',
            'slug',
            'description',
            'weight',
        ]


class FilterDelieriesForm(FilterForm):
    # TODO add relevant filters
    filter_field_list = [
        ('created', 'lt', 'date_to'),
        ('created', 'gt', 'date_from'),
    ]

    date_to = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={'class': 'datepicker'}),
    )
    date_from = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={'class': 'datepicker'}),
    )


class DeliveryUpdateForm(forms.ModelForm):

    status = forms.ChoiceField(
        choices=DeliveryStatus.choices(),
    )

    def save(self, commit=True):
        object = super().save(commit)

        if object.status == DeliveryStatus.SHIPPED.name:
            order = object.order
            order.status = OrderStatus.CLOSED.name
            order.save()

        return object

    class Meta:
        model = Delivery
        fields = [
            'status',
        ]
