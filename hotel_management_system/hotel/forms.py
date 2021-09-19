from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import NewUser


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField()


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = NewUser
        fields = "__all__"
