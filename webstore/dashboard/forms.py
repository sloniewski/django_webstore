from django import forms
from webstore.core.forms import FilterForm


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
