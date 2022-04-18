# Import the depenendencies for creating forms using django
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
# from .models import CustomUser
from django import forms
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError


class LoginForm(forms.Form):
    email = forms.CharField(widget = forms.EmailInput(attrs = {'class': 'form-control', 'placeholder' : 'Email'}))
    password = forms.CharField(widget = forms.PasswordInput(attrs = {'class': 'form-control', 'placeholder' : 'Password'}) )

# RegistrationForm class extends djangos UserCreationForm
class RegistrationForm(UserCreationForm):
    class Meta: 
        model = CustomUser
        fields = ('f_name', 'l_name', 'email', 'password')
    
               
class CustomUserChangeForm(UserChangeForm):
        class Meta:
            model = CustomUser
            fields = '__all__'