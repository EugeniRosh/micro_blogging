from __future__ import annotations

from typing import TYPE_CHECKING

from core.business_logic.services import trending_in_your_country
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.views.decorators.cache import cache_page
from django.views.decorators.http import require_http_methods

if TYPE_CHECKING:
    from django.http import HttpRequest, HttpResponse


@cache_page(60 * 60)
@login_required()
@require_http_methods(["GET"])
def trending_in_your_country_controller(request: HttpRequest) -> HttpResponse:
    trending_tags = trending_in_your_country(country=request.user.country)
    context = {"title": "Trending in country", "tags": trending_tags}
    return render(
        request=request, template_name="trending_in_country.html", context=context
    )
