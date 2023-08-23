from __future__ import annotations

from typing import TYPE_CHECKING

from core.bussiness_logic.exeptions import CreateUniqueError, GetValueError
from core.bussiness_logic.servises import (
    add_follow,
    edit_profile,
    get_followers,
    get_following,
    get_user_profile,
    parsing_create_unique_error_message,
    remove_follow,
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
def profile_users_controller(request: HttpRequest, username: str) -> HttpResponse:
    try:
        profile = get_user_profile(username=username)
    except GetValueError:
        return redirect(to="index")

    context = {"title": "Profile", "profile": profile}

    if request.user.username == username:
        return render(request=request, template_name="profile.html", context=context)

    return render(request=request, template_name="profile_users.html", context=context)


@login_required()
@require_http_methods(["GET"])
def profile_following_controller(request: HttpRequest, username: str) -> HttpResponse:
    following = get_following(username=username)
    context = {"title": "Following", "following": following}
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


@login_required()
@require_http_methods(["GET"])
def add_follow_controller(request: HttpRequest, username: str) -> HttpResponse:
    if username != request.user.username:
        try:
            add_follow(user=request.user, user_following=username)
        except GetValueError:
            return HttpResponseBadRequest(content="User does not exist")

    return redirect(to="profile_users", username=username)


@login_required()
@require_http_methods(["GET"])
def remove_follow_controller(request: HttpRequest, username: str) -> HttpResponse:
    if username != request.user.username:
        try:
            remove_follow(user=request.user, user_following=username)
        except GetValueError:
            return HttpResponseBadRequest(content="User does not exist")

    return redirect(to="profile_users", username=username)
