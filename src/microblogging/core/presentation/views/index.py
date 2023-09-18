from __future__ import annotations

from typing import TYPE_CHECKING

from core.business_logic.exceptions import PaginationError
from core.business_logic.services import get_twits_to_index_page
from core.presentation.paginator import CustomPaginator
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseBadRequest
from django.shortcuts import render
from django.views.decorators.http import require_http_methods

if TYPE_CHECKING:
    from django.http import HttpRequest, HttpResponse


@login_required
@require_http_methods(["GET"])
def index_controller(request: HttpRequest) -> HttpResponse:
    try:
        sort_string = request.GET["sort-string"]
    except KeyError:
        sort_string = "created_at"

    twits = get_twits_to_index_page(profile=request.user, sort_string=sort_string)
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
        "title": "MICROBLOG",
        "twits": twits_paginator,
        "sort_string": sort_string,
    }
    return render(request=request, template_name="index.html", context=context)
