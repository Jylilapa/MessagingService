from django.contrib.auth.forms import UserCreationForm
from django import forms

from recipients.forms import StyleFormMixin
from users.models import User


class UserRegisterForm(StyleFormMixin, UserCreationForm):
    class Meta:
        model = User
        fields = ["email", "password1", "password2"]


class UserModeratorForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = User
        fields = ["username", "email"]
