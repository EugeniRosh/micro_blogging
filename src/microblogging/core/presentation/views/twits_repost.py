from __future__ import annotations

from typing import TYPE_CHECKING

from core.bussiness_logic.exeptions import GetValueError
from core.bussiness_logic.servises import add_repost_twits, delete_repost_twits
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseBadRequest
from django.shortcuts import redirect
from django.views.decorators.http import require_http_methods

if TYPE_CHECKING:
    from django.http import HttpRequest, HttpResponse


@login_required()
@require_http_methods(["GET"])
def repost_twits_controller(request: HttpRequest, twit_id: int) -> HttpResponse:
    try:
        add_repost_twits(twit_id=twit_id, profile=request.user)
    except GetValueError:
        return HttpResponseBadRequest(content="Twit does not exist")

    return redirect(to="view_twit", twit_id=twit_id)


@login_required()
@require_http_methods(["GET"])
def twit_repost_deletion_controller(request: HttpRequest, twit_id: int) -> HttpResponse:
    try:
        delete_repost_twits(twit_id=twit_id, profile=request.user)
    except GetValueError:
        return HttpResponseBadRequest(content="Twit does not exist")

    return redirect(to="view_twit", twit_id=twit_id)
