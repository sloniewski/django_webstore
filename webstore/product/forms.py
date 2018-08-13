from django import forms

from webstore.core.forms import FilterForm
from .models import Category


class FilterProductsForm(FilterForm):
    filter_field_list = [
        ('categories', 'id__in', 'categories'),
    ]
    categories = forms.MultipleChoiceField(
        choices=Category.objects.form_choices,
        required=False,
        widget=forms.SelectMultiple(attrs={'class': 'browser-default'}),
    )
