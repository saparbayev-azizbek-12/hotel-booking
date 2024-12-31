from .models import CustomUser
from django.contrib.auth.forms import UserCreationForm
from django import forms

class UserRegisterForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'first_name', 'last_name', 'email', 'phone_number', 'password1', 'password2',]


class CustomUserEditForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['image', 'first_name', 'last_name', 'phone_number']

