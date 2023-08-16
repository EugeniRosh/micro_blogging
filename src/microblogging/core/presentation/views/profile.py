from __future__ import annotations

from typing import TYPE_CHECKING

from core.bussiness_logic.exeptions import GetValueError
from core.bussiness_logic.servises import get_followers, get_following, get_user_profile
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.views.decorators.http import require_http_methods

if TYPE_CHECKING:
    from django.http import HttpRequest, HttpResponse


@login_required()
@require_http_methods(["GET"])
def profile_controller(request: HttpRequest, username: str) -> HttpResponse:
    try:
        profile, followers_num = get_user_profile(username=username)
    except GetValueError:
        return redirect(to="index")

    context = {"title": "Profile", "profile": profile, "followers_num": followers_num}
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
