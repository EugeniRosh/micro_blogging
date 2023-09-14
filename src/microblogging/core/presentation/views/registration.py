from __future__ import annotations

from typing import TYPE_CHECKING

from core.business_logic.dto import RegistrationDTO
from core.business_logic.exceptions import (
    CreateUniqueError,
    ExpirationTimeError,
    GetValueError,
)
from core.business_logic.services import (
    convert_data_from_form_in_dacite,
    parsing_the_unique_creation_error_in_postgres,
    regisration_user,
    registration_confirmations,
)
from core.presentation.forms import RegistrationsForm
from django.http import HttpResponseBadRequest
from django.shortcuts import redirect, render
from django.utils.datastructures import MultiValueDictKeyError
from django.views.decorators.http import require_http_methods

if TYPE_CHECKING:
    from django.http import HttpRequest, HttpResponse


@require_http_methods(["GET", "POST"])
def registrations_controller(request: HttpRequest) -> HttpResponse:
    form = RegistrationsForm()
    context = {"title": "Registrations"}

    if request.POST:
        form_registration = RegistrationsForm(request.POST)
        if form_registration.is_valid():
            data = convert_data_from_form_in_dacite(
                dto=RegistrationDTO, data=form_registration.cleaned_data
            )
            try:
                regisration_user(data=data)
                context.update(
                    {"message": "Registration confirmation email has been sent to your"}
                )
                return render(
                    request=request, template_name="registrations.html", context=context
                )

            except CreateUniqueError as err:
                field = parsing_the_unique_creation_error_in_postgres(err=err)
                form = form_registration
                form.add_error(field=field, error=f"{field} already exists")

        else:
            form = form_registration

    context.update({"form": form})
    return render(request=request, template_name="registrations.html", context=context)


@require_http_methods(["GET"])
def registration_confirmations_controller(request: HttpRequest) -> HttpResponse:
    try:
        code_confirmation = request.GET["code"]
    except MultiValueDictKeyError:
        return HttpResponseBadRequest(content="Invalid request")

    try:
        registration_confirmations(confirmation_code=code_confirmation)
    except ExpirationTimeError:
        return HttpResponseBadRequest(content="Confirmation code expired.")
    except GetValueError:
        return HttpResponseBadRequest(content="Invalid confirmation code.")

    return redirect(to="index")
