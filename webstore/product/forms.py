from django import forms

from webstore.core.forms import FilterForm
from webstore.core.widgets import MaterializeSelectMultiple
from .models import Category


class FilterProductsForm(FilterForm):
    filter_field_list = [
        ('name', 'icontains', 'name'),
        ('description', 'icontains', 'description'),
        ('categories', 'id__in', 'categories'),
        ('weight', 'gte', 'weight_min'),
        ('weight', 'lte', 'weight_max'),
    ]

    name = forms.CharField(
        required=False,
    )

    categories = forms.MultipleChoiceField(
        choices=Category.objects.form_choices,
        required=False,
        widget=MaterializeSelectMultiple(),
    )
    description = forms.CharField(
        required=False,
    )
    weight_min = forms.FloatField(
        required=False,
    )
    weight_max = forms.FloatField(
        required=False,
    )
