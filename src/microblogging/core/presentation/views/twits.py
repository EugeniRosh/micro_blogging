from __future__ import annotations

from typing import TYPE_CHECKING

from core.bussiness_logic.dto import TwitsDTO
from core.bussiness_logic.exeptions import GetValueError, ProfileAccessError
from core.bussiness_logic.servises import (
    add_twits,
    convert_data_from_form_in_dacite,
    delete_twits,
    get_profile_like_on_twit,
    get_profile_repost_on_twit,
    view_twits,
)
from core.presentation.forms import TwitsForm
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseBadRequest
from django.shortcuts import redirect, render
from django.views.decorators.http import require_http_methods

if TYPE_CHECKING:
    from django.http import HttpRequest, HttpResponse


@login_required()
@require_http_methods(["GET", "POST"])
def add_twits_controller(request: HttpRequest) -> HttpResponse:
    form = TwitsForm()

    if request.POST:
        form_twits = TwitsForm(request.POST)
        if form_twits.is_valid():
            data = convert_data_from_form_in_dacite(
                dto=TwitsDTO, data=form_twits.cleaned_data
            )
            twit = add_twits(data=data, profile=request.user)
            return redirect(to="view_twit", twit_id=twit.id)
        else:
            form = form_twits

    context = {"title": "Add", "form": form}
    return render(request=request, template_name="twits_add.html", context=context)


@login_required()
@require_http_methods(["GET"])
def view_twits_controller(request: HttpRequest, twit_id: int) -> HttpResponse:
    try:
        twit, tags, twits_ansver = view_twits(twit_id=twit_id)
    except GetValueError:
        return HttpResponseBadRequest(content="Twit does not exist")

    profile = request.user

    if profile != twit.profile:
        like_twit = get_profile_like_on_twit(profile=profile, twit=twit)
        repost_twit = get_profile_repost_on_twit(profile=profile, twit=twit)
    else:
        like_twit = None
        repost_twit = None

    context = {
        "title": "View twit",
        "twit": twit,
        "tags": tags,
        "like_twit": like_twit,
        "repost_twit": repost_twit,
        "twits_ansver": twits_ansver,
    }

    return render(request=request, template_name="twits_view.html", context=context)


@login_required()
@require_http_methods(["GET"])
def delete_twits_controller(request: HttpRequest, twit_id: int) -> HttpResponse:
    try:
        delete_twits(twit_id=twit_id, profile=request.user)
    except GetValueError:
        return HttpResponseBadRequest(content="Twit does not exist")
    except ProfileAccessError:
        return HttpResponseBadRequest(content="No access rights")

    return redirect(to="profile_users", username=request.user.username)
