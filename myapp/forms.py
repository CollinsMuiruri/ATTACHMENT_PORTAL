from django.contrib.auth.forms import AuthenticationForm, UsernameField
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction
from .models import Course
from django import forms

from .models import User

class UserLoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(UserLoginForm, self).__init__(*args, **kwargs)

    username = UsernameField(
        widget=forms.TextInput(attrs={"placeholder": "e.g. 2100001", "required": True})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "•••••••••••••",
                "id": "password-input",
            }
        )
    )