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
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseBadRequest
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
@require_http_methods(["GET"])
def profile_edit_controller(request: HttpRequest) -> HttpResponse:
    context = {"title": "Edit profile"}
    return render(request=request, template_name="edit_profile.html", context=context)


@login_required()
@require_http_methods(["GET", "POST"])
def edit_field_profile_controller(request: HttpRequest, field: str) -> HttpResponse:
    context = {"title": "Edit field"}
    try:
        initial = {field: getattr(request.user, field)}
    except AttributeError:
        return HttpResponseBadRequest(content="Invalid edit request")

    try:
        form = get_edit_form(field=field, initial=initial)
    except GetValueError:
        HttpResponseBadRequest(content="Invalid edit request")

    if request.POST:
        form = get_edit_form(
            field=field, data=request.POST, files=request.FILES, initial=initial
        )
        if form.has_changed():
            if form.is_valid():
                try:
                    data = form.cleaned_data
                    edit_profile(
                        username=request.user.username,
                        data=data,
                        files=request.FILES,
                    )
                    request.user.refresh_from_db()
                    return redirect(to="edit_profile")

                except CreateUniqueError as err:
                    field = parsing_create_unique_error_message(err=err)
                    form.add_error(field=field, error=f"{field} already exists")
        else:
            redirect(to="edit_profile")

    context.update({"form": form})
    return render(
        request=request, template_name="edit_field_profile.html", context=context
    )
