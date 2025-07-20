from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

User = get_user_model()


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    fieldsets = BaseUserAdmin.fieldsets + (
        (_("Additional Info"), {"fields": ("full_name", "bio")}),
    )
    list_display = ("username", "email", "full_name", "is_staff")
    search_fields = ("username", "email", "full_name")