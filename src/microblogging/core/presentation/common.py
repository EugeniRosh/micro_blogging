from __future__ import annotations

from typing import TYPE_CHECKING, Any

from core.bussiness_logic.exeptions import GetValueError
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
    from django.forms import Form
    from django.utils.datastructures import MultiValueDict


def get_edit_form(
    field: str,
    data: MultiValueDict = None,
    files: MultiValueDict = None,
    initial: dict[str, Any] | None = None,
) -> Form:
    form: Form = None

    if "first_name" == field:
        form = EditProfileFirstNameForm(data=data, initial=initial)
    elif "last_name" == field:
        form = EditProfileLastNameForm(data=data, initial=initial)
    elif "username" == field:
        form = EditProfileUsernameForm(data=data, initial=initial)
    elif "email" == field:
        form = EditProfileEmailForm(data=data, initial=initial)
    elif "country" == field:
        form = EditProfileCountryForm(data=data, initial=initial)
    elif "photo" == field:
        form = EditProfilePhotoForm(data=data, files=files)
    elif "description" == field:
        form = EditProfileDescriptionForm(data=data, initial=initial)
    elif "date_of_birth" == field:
        form = EditProfileDateOfBirthForm(data=data, initial=initial)
    else:
        raise GetValueError

    return form
