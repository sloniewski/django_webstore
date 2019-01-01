from django import forms
from django.contrib.auth import get_user_model

import django_filters

User = get_user_model()


class FilterUsersForm(django_filters.FilterSet):
    first_name = django_filters.CharFilter(
        field_name='first_name',
        lookup_expr='icontains',
    )
    last_name = django_filters.CharFilter(
        field_name='last_name',
        lookup_expr='icontains',
    )
    email = django_filters.CharFilter(
        field_name='email',
        lookup_expr='icontains',
    )

    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'email',
            'is_staff',
            'is_active',
        ]


class BaseUserBulkActionMixin(forms.Form):
    object_list = forms.ModelMultipleChoiceField(
        queryset=None,
        widget=forms.CheckboxSelectMultiple()
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._meta = self.get_meta()
        self.fields['object_list'].queryset = self.get_queryset()

    def get_meta(self):
        return self.Meta()

    def get_queryset(self):
        return self._meta.model.objects.all()

    def execute(self):
        raise NotImplementedError('method not implemented')

    def get_message(self):
        raise NotImplementedError('success message not provided')

    class Meta:
        model = User


class BulkDeleteForm(BaseUserBulkActionMixin):

    def execute(self):
        for object in self.cleaned_data['object_list']:
            object.delete()
        return True

    def get_message(self):
        return 'Deleted selected users'


class BulkActivateForm(BaseUserBulkActionMixin):

    def execute(self):
        self.cleaned_data['object_list'].update(is_active=True)
        return True

    def get_message(self):
        return 'Activated selected users'


class BulkDeactivateForm(BaseUserBulkActionMixin):

    def execute(self):
        self.cleaned_data['object_list'].update(is_active=False)
        return True

    def get_message(self):
        return 'Deactivated selected users'


UserBulkActions = {
    'delete': BulkDeleteForm,
    'activate': BulkActivateForm,
    'deactivate': BulkDeactivateForm,
}
