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


class FilterPaymentsForm(FilterForm):
    filter_field_list = [
        ('created', 'lt', 'date_to'),
        ('created', 'gt', 'date_from'),
        ('value', 'float__lt', 'value_to'),
        ('value', 'float__gt', 'value_from'),
    ]

    date_to = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={'class': 'datepicker'}),
    )
    date_from = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={'class': 'datepicker'}),
    )
    value_from = forms.FloatField(
        required=False,
        min_value=0,
    )
    value_to = forms.FloatField(
        required=False,
        min_value=0,
    )


class UpdatePaymentForm(forms.ModelForm):
    send_mail = forms.BooleanField(
        label='send mail to client',
        required=False,
        widget=MaterializeCheckboxInput(
            attrs={
                'class': 'filled-in',
                'checked': 'checked',
            }
        )
    )

    def save(self, commit=True):
        object = super().save(commit)
        if object.status == PaymentStatus.CLOSED.name:
            delivery = object.order.delivery
            delivery.status = DeliveryStatus.READY_FOR_SHIPPING.name
            delivery.save()

            order = object.order
            order.status = OrderStatus.SHIPPING.name
            order.save()

        if object.status in [PaymentStatus.OPEN.name, PaymentStatus.DELAYED.name]:
            delivery = object.order.delivery
            delivery.status = DeliveryStatus.AWAITING_PAYMENT.name
            delivery.save()

            order = object.order
            order.status = OrderStatus.AWAITING_PAYMENT.name
            order.save()

        send_mail_flag = self.cleaned_data.get('send_mail')
        if send_mail_flag is True:
            send_mail(
                subject='Payment status for order: {}'.format(object.order.id),
                message='Payment status was updated to: {}'.format(object.status),
                from_email='placeholder@test.com',
                recipient_list=[object.order.user.email],
                fail_silently=False,
            )
        return object

    class Meta:
        model = Payment
        fields = [
            'status',
        ]


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
