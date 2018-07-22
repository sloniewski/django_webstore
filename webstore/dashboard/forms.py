from django import forms
from django.core.mail import send_mail

from webstore.core.forms import FilterForm
from webstore.payment.models import Payment


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
        widget=forms.CheckboxInput(
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
            'status',
        ]
