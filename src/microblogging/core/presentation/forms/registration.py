from core.presentation.validators import ValidationAge
from django import forms
from django.contrib.auth.password_validation import validate_password


class RegistrationsForm(forms.Form):
    username = forms.CharField(label="Username")
    email = forms.EmailField(label="Email")
    password = forms.CharField(
        label="Password", widget=forms.PasswordInput, validators=[validate_password]
    )
    date_of_birth = forms.DateTimeField(
        label="Date of birth",
        help_text="format: 01.01.0001",
        input_formats=["%d.%m.%Y"],
        validators=[ValidationAge(min_age=18)],
    )
