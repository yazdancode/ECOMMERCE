from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group

from accounts.forms import UserChangeForm, UserCreationForm
from accounts.models import OtpCode, User


class UserAdmin(BaseUserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm
    list_display = ("email", "phone_number", "fullname", "is_admin")
    list_filter = ("is_admin",)
    fieldsets = (
        (None, {"fields": ("email", "phone_number", "fullname", "password")}),
        ("Permissions", {"fields": ("is_active", "is_admin", "last_login")}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "email",
                    "phone_number",
                    "fullname",
                    "password1",
                    "password2",
                ),
            },
        ),
    )
    search_fields = ("email", "fullname")
    ordering = ("fullname",)
    filter_horizontal = ()


admin.site.unregister(Group)
admin.site.register(User, UserAdmin)


@admin.register(OtpCode)
class OtpAdmin(admin.ModelAdmin):
    list_display = ("phone", "code", "created_at")
