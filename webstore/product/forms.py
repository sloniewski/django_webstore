from django import forms

from webstore.core.forms import FilterForm
from webstore.core.widgets import MaterializeSelectMultiple
from .models import Category


class FilterProductsForm(FilterForm):
    filter_field_list = [
        ('categories', 'id__in', 'categories'),
    ]
    categories = forms.MultipleChoiceField(
        choices=Category.objects.form_choices,
        required=False,
        widget=MaterializeSelectMultiple(
            attrs={'class': 'browser-default'}
        ),
    )
