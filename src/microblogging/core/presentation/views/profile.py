from __future__ import annotations

from typing import TYPE_CHECKING

from core.bussiness_logic.exeptions import GetValueError
from core.bussiness_logic.servises import get_user_profile
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
