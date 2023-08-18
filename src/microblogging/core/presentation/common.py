from __future__ import annotations

from typing import TYPE_CHECKING

from core.presentation.forms import (
    EditProfileCountryForm,
    EditProfileDateOfBirthForm,
    EditProfileDescriptionForm,
    EditProfileEmailForm,
    EditProfileFirstNameForm,
    EditProfileLastNameForm,
    EditProfilePhotoForm,
    EditProfileUsernameForm,
)

if TYPE_CHECKING:
    from core.models import Profiles
    from django.forms import Form
    from django.http import QueryDict
    from django.utils.datastructures import MultiValueDict


def get_edit_form(data: QueryDict, files: MultiValueDict, user: Profiles) -> Form:
    field = list(data)[-1]
    initial = {field: getattr(user, field)}

    form: Form = None

    if "first_name" in data:
        form = EditProfileFirstNameForm(data=data, initial=initial)
    elif "last_name" in data:
        form = EditProfileLastNameForm(data=data, initial=initial)
    elif "username" in data:
        form = EditProfileUsernameForm(data=data, initial=initial)
    elif "email" in data:
        form == EditProfileEmailForm(data=data, initial=initial)
    elif "country" in data:
        form = EditProfileCountryForm(data, initial=initial)
    elif "photo" in files:
        form = EditProfilePhotoForm(data=data, files=files)
    elif "description" in data:
        form = EditProfileDescriptionForm(data=data, initial=initial)
    elif "date_of_birth" in data:
        form = EditProfileDateOfBirthForm(data=data, initial=initial)

    return form
