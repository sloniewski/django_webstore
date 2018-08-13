from django.forms.widgets import SelectMultiple


class MaterializeSelectMultiple(SelectMultiple):
    template_name = 'materialize_checkbox_select.html'
