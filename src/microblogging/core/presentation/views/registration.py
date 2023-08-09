from __future__ import annotations

from typing import TYPE_CHECKING

from core.bussiness_logic.dto import RegistrationDTO
from core.bussiness_logic.exeptions import CreateUniqueError
from core.bussiness_logic.servises import (
    convert_data_from_form_in_dacite,
    parsing_create_unique_error_message,
    regisration_user,
)
from core.presentation.forms import RegistrationsForm
from django.shortcuts import render
from django.views.decorators.http import require_http_methods

if TYPE_CHECKING:
    from django.http import HttpRequest, HttpResponse


@require_http_methods(["GET", "POST"])
def registrations_controller(request: HttpRequest) -> HttpResponse:
    form = RegistrationsForm()
    if request.POST:
        form_registration = RegistrationsForm(request.POST)
        if form_registration.is_valid():
            data = convert_data_from_form_in_dacite(
                dto=RegistrationDTO, data=form_registration.cleaned_data
            )
            try:
                regisration_user(data=data)
                context = {
                    "title": "Registrations",
                    "message": "Registration confirmation email has been sent to your",
                }
                return render(
                    request=request, template_name="registrations.html", context=context
                )

            except CreateUniqueError as err:
                field = parsing_create_unique_error_message(err=err)
                form = form_registration
                form.add_error(field=field, error=f"{field} already exists")

        else:
            form = form_registration

    context = {"title": "Registrations", "form": form}
    return render(request=request, template_name="registrations.html", context=context)
