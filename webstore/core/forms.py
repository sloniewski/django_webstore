from django import forms
from django.db.models import Q


class FilterForm(forms.Form):
    filter_field_list = None

    def create_Q(self, param, operator, field_name):
        """
        creates a Q object from a form field,
        `param` is used as lhs of lookup
        `operator` is the rhs part of lookup
        'field_name` refers to form field
        """
        key = '{}__{}'.format(param, operator)
        value = self.cleaned_data.get(field_name)
        if value not in [None, '', False, []]:
            return Q(**{key: value})
        return None

    def get_filters(self):
        """
        returns a list of Q objects,basing on fields listed in `filter_field_list`
        and using `create_Q` method
        """
        filters = []
        for item in self.filter_field_list:
            new_Q = self.create_Q(
                param=item[0],
                operator=item[1],
                field_name=item[2],
            )
            if new_Q is not None:
                filters.append(new_Q)

        return filters
