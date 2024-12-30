from .models import CustomUser, Profile
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

class UserRegisterForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'first_name', 'last_name', 'email', 'phone_number', 'password1', 'password2',]

class UserEditForm(UserChangeForm):
    class Meta:
        model = Profile
        fields = ['img', 'first_name', 'last_name', 'phone_number']
