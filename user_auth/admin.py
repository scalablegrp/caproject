from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group
from .models import CustomUser
from .forms import RegistrationForm, CustomUserChangeForm


class CustomUserAdmin(BaseUserAdmin):
    add_form = RegistrationForm
    form = CustomUserChangeForm
    model = CustomUser
    ordering = ('email',)
    # The fields to be used in displaying the User model.
    list_display = ['f_name', 'l_name', 'email', 'member_since', 'last_login', 'is_admin', 'is_staff', 'is_superuser']


admin.site.register(CustomUser, CustomUserAdmin)