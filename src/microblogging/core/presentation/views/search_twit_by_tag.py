from __future__ import annotations

from typing import TYPE_CHECKING

from core.business_logic.dto import TagsSearchDTO
from core.business_logic.exceptions import PaginationError
from core.business_logic.services import (
    convert_data_from_form_in_dacite,
    get_twits_by_tag,
)
from core.presentation.forms import TagsSearchForm
from core.presentation.paginator import CustomPaginator
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseBadRequest
from django.shortcuts import render
from django.views.decorators.http import require_http_methods

if TYPE_CHECKING:
    from django.http import HttpRequest, HttpResponse


@login_required()
@require_http_methods(["GET"])
def get_twits_by_tag_controller(request: HttpRequest) -> HttpResponse:
    twits_paginator = None
    form = TagsSearchForm()
    tag = ""

    form_search = TagsSearchForm(data=request.GET)
    if form_search.is_valid():
        data = convert_data_from_form_in_dacite(
            dto=TagsSearchDTO, data=form_search.cleaned_data
        )
        twits = get_twits_by_tag(data=data)
        tag = data.tag


        try:
            page_num = request.GET["page"]
        except KeyError:
            page_num = 1

        paginator = CustomPaginator(max_value=20)

        try:
            twits_paginator = paginator.paginate(data=twits, page_num=page_num)
        except PaginationError:
            return HttpResponseBadRequest(
                content="Page with provided number doesn't exist."
            )

    context = {
        "title": "Tags",
        "form": form,
        "twits": twits_paginator,
        "tag": tag,

    }
    return render(
        request=request, template_name="search_twit_by_tag.html", context=context
    )
