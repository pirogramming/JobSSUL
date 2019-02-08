from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.forms import UserCreationForm,UserChangeForm
from .models import User


class LoginForm(AuthenticationForm):
    pass


class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm):
        model = User
        fields = ['name', 'nickname', 'email',]



