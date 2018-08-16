from django.forms.widgets import CheckboxSelectMultiple


class MaterializeSelectMultiple(CheckboxSelectMultiple):
    option_template_name = 'widgets/materialize_input_option.html'

    def get_context(self, name, value, attrs):
        context = super().get_context(name, value, attrs)
        context['wrap_label'] = True
        return context
