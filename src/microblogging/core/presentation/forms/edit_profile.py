from core.presentation.validators import ValidationAge
from django import forms


class EditProfileFirstNameForm(forms.Form):
    first_name = forms.CharField(
        label="Name", max_length=100, required=False, strip=True
    )


class EditProfileLastNameForm(forms.Form):
    last_name = forms.CharField(
        label="Surname", max_length=100, required=False, strip=True
    )


class EditProfileUsernameForm(forms.Form):
    username = forms.CharField(label="Username", max_length=100, strip=True)


class EditProfilePasswordForm(forms.Form):
    password = forms.CharField(label="Password", strip=True)


class EditProfileEmailForm(forms.Form):
    email = forms.EmailField(label="Email", max_length=100)


class EditProfileCountryForm(forms.Form):
    country = forms.CharField(
        label="Country", max_length=100, required=False, strip=True
    )


class EditProfilePhotoForm(forms.Form):
    photo = forms.ImageField(label="Photo", initial='')


class EditProfileDescriptionForm(forms.Form):
    description = forms.CharField(
        label="Description",
        max_length=200,
        required=False,
        strip=True,
        widget=forms.Textarea,
    )


class EditProfileDateOfBirthForm(forms.Form):
    date_of_birth = forms.DateTimeField(
        label="Date of birth",
        help_text="format: 01.01.0001",
        input_formats=["%d.%m.%Y"],
        validators=[ValidationAge(min_age=18)],
    )
