from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class RegistrationForm(UserCreationForm):
    # add additional fields
    email = forms.EmailField()
    first_name = forms.CharField()
    last_name = forms.CharField()

    # include Meta class
    class Meta:
        model = User
        fields = ["username", "first_name", "last_name", "email", "password1", "password2"]