import django_filters
from django import forms
from django.core.mail import send_mail

from webstore.core.widgets import MaterializeCheckboxInput
from webstore.payment.models import Payment


class FilterPaymentForm(django_filters.FilterSet):
    created_before = django_filters.DateFilter(
        field_name='created',
        lookup_expr='lte',
        label='Created before',
    )
    created_after = django_filters.DateFilter(
        field_name='created',
        lookup_expr='gte',
        label='Created after',
    )
    value_gte = django_filters.NumberFilter(
        field_name='value',
        lookup_expr='gte',
        label='value greater than',
    )
    value_lte = django_filters.NumberFilter(
        field_name='value',
        lookup_expr='lte',
        label='value less than',
    )

    class Meta:
        model = Payment
        fields = [
            'payed',
        ]


class UpdatePaymentForm(forms.ModelForm):
    send_mail = forms.BooleanField(
        label='Send mail to client',
        required=False,
        widget=MaterializeCheckboxInput(
            attrs={
                'class': 'filled-in',
                'checked': 'checked',
            }
        )
    )

    payed = forms.BooleanField(
        label='Payment recived',
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
            'payed',
        ]