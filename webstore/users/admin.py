from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import CustomUser


def deactivate(modeladmin, request, queryset):
    queryset.update(is_active=False)


def activate(modeladmin, request, queryset):
    queryset.update(is_active=True)


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display = [
        'username',
        'last_login',
        'email',
        'is_staff',
        'is_active',
    ]
    list_filter = ('is_staff', 'is_active', 'last_login')
    actions = [
        deactivate,
        activate
    ]

