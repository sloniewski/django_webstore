from django import forms
from django.db.models import Q

from .models import Category


class FilterProductsForm(forms.Form):
    category = forms.ChoiceField(
        choices=[],
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['category'].choices = [x.form_choice for x in Category.objects.all()]

    def get_filters(self):
        """
        :return: list of Q objects
        """
        filters = []

        category = self.cleaned_data['category']

        filters.append(Q(category__name=category))
        return filters
