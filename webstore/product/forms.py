from django import forms
from django.db.models import Q, F , FloatField, IntegerField
from django.db.models.functions import Cast

from .models import Category


class FilterProductsForm(forms.Form):
    category = forms.ChoiceField(
        choices=[
            ('All', 'All'),
        ],
        required=False,
        validators=[]
    )
    price_min = forms.FloatField(
        min_value=0,
        label='min price',
        required=False,
    )
    price_max = forms.FloatField(
        min_value=0,
        label='max price',
        required=False
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        saved_category_choices = [x.form_choice for x in Category.objects.all()]
        self.fields['category'].choices += saved_category_choices

    def get_filters(self):
        """
        :return: list of Q objects
        """
        filters = []

        #TODO this part needs refactoring
        category = self.data.get('category')
        if category not in [None, '', 'All']:
            filters.append(Q(category__name=category))

        price_min = self.data.get('price_min')
        price_max = self.data.get('price_max')

        if price_min not in [None, '', False]:
            filters.append(Q(price__value__float__gte=price_min))

        if price_max not in [None, '', False]:
            filters.append(Q(price__value__float__lte=price_max))

        return filters
