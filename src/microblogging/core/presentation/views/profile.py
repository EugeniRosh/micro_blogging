from __future__ import annotations

from typing import TYPE_CHECKING

from core.business_logic.exceptions import (
    CreateUniqueError,
    GetValueError,
    PaginationError,
)
from core.business_logic.services import (
    add_follow,
    edit_profile,
    get_all_followers,
    get_all_following,
    get_profile,
    get_twits_and_reposts,
    parsing_the_unique_creation_error_in_postgres,
    remove_follow,
)
from core.presentation.common import get_edit_form
from core.presentation.paginator import CustomPaginator
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseBadRequest
from django.shortcuts import redirect, render
from django.views.decorators.http import require_http_methods

if TYPE_CHECKING:
    from django.http import HttpRequest, HttpResponse


@login_required()
@require_http_methods(["GET"])
def profile_users_controller(request: HttpRequest, username: str) -> HttpResponse:
    if request.user.username == username:
        return redirect(to="my_profile")

    try:
        page_num = request.GET["page"]
    except KeyError:
        page_num = 1

    try:
        profile, twits, follow = get_profile(username=username)
    except GetValueError:
        return redirect(to="index")

    paginator = CustomPaginator(max_value=20)
    try:
        twits_paginator = paginator.paginate(data=twits, page_num=page_num)
    except PaginationError:
        return HttpResponseBadRequest(
            content="Page with provided number doesn't exist."
        )

    context = {
        "title": "Profile",
        "profile": profile,
        "twits": twits_paginator,
        "follow": follow,
    }
    return render(request=request, template_name="profile_users.html", context=context)


@login_required()
@require_http_methods(["GET"])
def my_profile_controller(request: HttpRequest) -> HttpResponse:
    profile = request.user

    try:
        page_num = request.GET["page"]
    except KeyError:
        page_num = 1

    twits = get_twits_and_reposts(profile=profile)

    paginator = CustomPaginator(max_value=20)
    try:
        twits_paginator = paginator.paginate(data=twits, page_num=page_num)
    except PaginationError:
        return HttpResponseBadRequest(
            content="Page with provided number doesn't exist."
        )

    context = {"title": "Profile", "profile": profile, "twits": twits_paginator}
    return render(request=request, template_name="profile.html", context=context)


@login_required()
@require_http_methods(["GET"])
def receiving_profile_followings_controller(
    request: HttpRequest, username: str
) -> HttpResponse:
    following = get_all_following(username=username)
    context = {"title": "Following", "following": following}
    return render(
        request=request, template_name="profile_followings.html", context=context
    )


@login_required()
@require_http_methods(["GET"])
def get_followers_profile_controller(
    request: HttpRequest, username: str
) -> HttpResponse:
    followers = get_all_followers(username=username)
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
                    field = parsing_the_unique_creation_error_in_postgres(err=err)
                    form.add_error(field=field, error=f"{field} already exists")
        else:
            redirect(to="edit_profile")

    context.update({"form": form})
    return render(
        request=request, template_name="edit_field_profile.html", context=context
    )


@login_required()
@require_http_methods(["GET"])
def adding_a_follower_profile_controller(
    request: HttpRequest, username: str
) -> HttpResponse:
    if username != request.user.username:
        try:
            add_follow(user=request.user, user_following=username)
        except GetValueError:
            return HttpResponseBadRequest(content="User does not exist")

    return redirect(to="profile_users", username=username)


@login_required()
@require_http_methods(["GET"])
def follower_profile_removal_controller(
    request: HttpRequest, username: str
) -> HttpResponse:
    if username != request.user.username:
        try:
            remove_follow(user=request.user, user_following=username)
        except GetValueError:
            return HttpResponseBadRequest(content="User does not exist")

    return redirect(to="profile_users", username=username)
