from allauth.account.forms import SignupForm
from django.contrib.auth.models import Group, User
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.db import models

class BaseRegisterForm(UserCreationForm):
    email = forms.EmailField(label="Email")
    first_name = forms.CharField(label="Имя")
    last_name = forms.CharField(label="Фамилия")

    class Meta:
        model = User
        fields = ("username",
                  "first_name",
                  "last_name",
                  "email",
                  "password1",
                  "password2",)

class ValidationForm(forms.Form):
    validationCode = forms.CharField(label='Enter Six-Digit validation code', label_suffix=" : ", min_length=6, max_length=6,
                           required=True,
                           widget=forms.TextInput(attrs={'class': 'form-control'}),
                           help_text="Please enter the validation code.",
                           error_messages={'required': "Please Enter your validation code"}, disabled=False, strip=True)