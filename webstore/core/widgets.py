from django.forms.widgets import CheckboxSelectMultiple, CheckboxInput


class MaterializeSelectMultiple(CheckboxSelectMultiple):
    option_template_name = 'webstore/widgets/materialize_input_option.html'

    def get_context(self, name, value, attrs):
        context = super().get_context(name, value, attrs)
        context['wrap_label'] = True
        return context


class MaterializeCheckboxInput(CheckboxInput):
    template_name = 'webstore/widgets/materialize_input_option.html'

    def get_context(self, name, value, attrs):
        context = super().get_context(name, value, attrs)
        context['wrap_label'] = True
        return context
