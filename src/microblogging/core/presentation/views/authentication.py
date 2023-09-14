from __future__ import annotations

from typing import TYPE_CHECKING

from core.business_logic.dto import AuthenticationDTO
from core.business_logic.exceptions import GetValueError
from core.business_logic.services import (
    authentication_user,
    convert_data_from_form_in_dacite,
    logout_user,
)
from core.presentation.forms import AuthenticationForm
from django.shortcuts import redirect, render
from django.views.decorators.http import require_http_methods

if TYPE_CHECKING:
    from django.http import HttpRequest, HttpResponse


@require_http_methods(["GET", "POST"])
def authentication_controller(request: HttpRequest) -> HttpResponse:
    form = AuthenticationForm()

    context = {"title": "Authentication"}

    if request.POST:
        form_authentication = AuthenticationForm(request.POST)
        if form_authentication.is_valid():
            data = convert_data_from_form_in_dacite(
                dto=AuthenticationDTO, data=form_authentication.cleaned_data
            )
            try:
                authentication_user(request=request, data=data)
                return redirect(to="index")
            except GetValueError:
                form = form_authentication
                context.update({"message": "Incorrect email or password."})
        else:
            form = form_authentication

    context.update({"form": form})
    return render(request=request, template_name="authentication.html", context=context)


@require_http_methods(["GET"])
def logout_controller(request: HttpRequest) -> HttpResponse:
    logout_user(request=request)
    return redirect(to="index")
