from django.contrib import admin

from .models import CustomUser


def deactivate(modeladmin, request, queryset):
    queryset.update(is_active=False)


def activate(modeladmin, request, queryset):
    queryset.update(is_active=True)


@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = [
        'username',
        'last_login',
        'email',
        'is_staff',
        'is_active',
    ]
    list_filter = ('is_staff', 'is_active')
    actions = [
        deactivate,
        activate
    ]
