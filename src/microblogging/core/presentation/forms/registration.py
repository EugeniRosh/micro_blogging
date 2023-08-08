from core.presentation.validators import ValidationAge
from django import forms


class RegistrationsForm(forms.Form):
    username = forms.CharField(label="Username")
    email = forms.EmailField(label="Email")
    password = forms.CharField(label="Password", widget=forms.PasswordInput)
    date_of_birth = forms.DateTimeField(
        label="Date of birth",
        help_text="format: 01.01.0001",
        input_formats=["%d.%m.%Y"],
        validators=[ValidationAge(min_age=18)],
    )
