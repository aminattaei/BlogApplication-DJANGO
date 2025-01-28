from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import CustomUser
from .forms import CustomUserCreationForm, CustomUserChangeForm


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ["username", "phone_number",'email']
    fieldsets = UserAdmin.fieldsets + (
    (
        None,
        {
            "fields": ("phone_number",),  
        },
    ),
    )

    add_fieldsets = UserAdmin.add_fieldsets + (
        (
            None,
            {
                "fields": ("phone_number",),  
            },
        ),
    )


admin.site.register(CustomUser,CustomUserAdmin)