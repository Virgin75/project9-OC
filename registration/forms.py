from django import forms
from django.contrib.auth.forms import UserCreationForm
from registration.models import User
from django.db import models


class RegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ["email", "password1", "password2"]


class SignInForm(forms.Form):
    email = forms.EmailField(max_length=254)
    password = forms.CharField(max_length=32, widget=forms.PasswordInput)
