from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import get_user_model

from accountApp.models import CustomUser


class LoginForm(AuthenticationForm):
    class Meta:
        fields = ['username', 'password']


class SignUpForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = [
            'username', 'password1', 'password2', 'email', 'nickname',
            'introduce', 'image'
        ]
