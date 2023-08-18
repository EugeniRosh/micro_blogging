from __future__ import annotations

from typing import TYPE_CHECKING

from core.bussiness_logic.exeptions import CreateUniqueError, GetValueError
from core.bussiness_logic.servises import (
    edit_profile,
    get_followers,
    get_following,
    get_user_profile,
    parsing_create_unique_error_message,
)
from core.presentation.common import get_edit_form
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
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.views.decorators.http import require_http_methods

if TYPE_CHECKING:
    from django.http import HttpRequest, HttpResponse


@login_required()
@require_http_methods(["GET"])
def profile_controller(request: HttpRequest, username: str) -> HttpResponse:
    try:
        profile = get_user_profile(username=username)
    except GetValueError:
        return redirect(to="index")

    context = {"title": "Profile", "profile": profile}
    return render(request=request, template_name="profile.html", context=context)


@login_required()
@require_http_methods(["GET"])
def profile_following_controller(request: HttpRequest, username: str) -> HttpResponse:
    following = get_following(username=username)
    context = {"title": "Following", "following": following}
    print(following)
    return render(
        request=request, template_name="profile_followings.html", context=context
    )


@login_required()
@require_http_methods(["GET"])
def profile_followers_controller(request: HttpRequest, username: str) -> HttpResponse:
    followers = get_followers(username=username)
    context = {"title": "Followers", "followers": followers}
    return render(
        request=request, template_name="profile_followers.html", context=context
    )


@login_required()
@require_http_methods(["GET", "POST"])
def profile_edit_controller(request: HttpRequest) -> HttpResponse:
    context = {"title": "Edit profile"}
    if request.POST:
        form = get_edit_form(data=request.POST, files=request.FILES, user=request.user)
        if form.has_changed():
            if form.is_valid():
                try:
                    edit_profile(
                        username=request.user.username,
                        data=request.POST,
                        files=request.FILES,
                    )
                    request.user.refresh_from_db()
                except CreateUniqueError as err:
                    field = parsing_create_unique_error_message(err=err)
                    context.update({"message": f"{field} already exists"})

    first_name_form = EditProfileFirstNameForm({"first_name": request.user.first_name})
    last_name_form = EditProfileLastNameForm({"last_name": request.user.last_name})
    username_form = EditProfileUsernameForm({"username": request.user.username})
    email_form = EditProfileEmailForm({"email": request.user.email})
    country_form = EditProfileCountryForm({"country": request.user.country})
    photo_form = EditProfilePhotoForm({"photo": request.user.photo})
    description_form = EditProfileDescriptionForm(
        {"description": request.user.description}
    )
    date_of_birth_form = EditProfileDateOfBirthForm(
        {
            "date_of_birth": (
                f"{request.user.date_of_birth.day}."
                f"{request.user.date_of_birth.month}."
                f"{request.user.date_of_birth.year}"
            )
        }
    )

    context.update(
        {
            "first_name_form": first_name_form,
            "last_name_form": last_name_form,
            "username_form": username_form,
            "email_form": email_form,
            "country_form": country_form,
            "photo_form": photo_form,
            "description_form": description_form,
            "date_of_birth_form": date_of_birth_form,
        }
    )
    return render(request=request, template_name="edit_profile.html", context=context)
