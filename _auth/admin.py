from django.contrib import admin
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _
from .models import User, EmailVerificationToken, ResetPasswordToken


# Register your models here.
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {"fields": ("image",)}),
        (_("Profile"), {"fields": ("email", "phone_number")}),
        (
            _("Personal info"),
            {
                "fields": (
                    "full_name",
                )
            },
        ),

        (
            _("Meta Information"),
            {
                "fields": (
                    "is_email_verified",
                    "account_type",
                    "badges"
                )
            },
        ),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        (_("Important dates"), {"fields": ("last_login", "date_joined")}),
    )
    list_display = ['id', 'email', 'full_name', 'account_type', 'is_superuser']
    search_fields = ["email"]
    readonly_fields = ["account_type"]

admin.site.register(EmailVerificationToken)
admin.site.register(ResetPasswordToken)