from __future__ import annotations

from typing import TYPE_CHECKING

from core.bussiness_logic.dto import TwitsDTO
from core.bussiness_logic.servises import add_twits, convert_data_from_form_in_dacite
from core.presentation.forms import TwitsForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
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
            add_twits(data=data, profile=request.user)
        else:
            form = form_twits

    context = {"title": "Add", "form": form}
    return render(request=request, template_name="add_twits.html", context=context)
