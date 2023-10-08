from __future__ import annotations

from typing import TYPE_CHECKING

from core.business_logic.services import get_user_notifications
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.views.decorators.http import require_http_methods

if TYPE_CHECKING:
    from django.http import HttpRequest, HttpResponse


@login_required
@require_http_methods(["GET"])
def get_user_notifications_controller(request: HttpRequest) -> HttpResponse:
    notifications = get_user_notifications(profile=request.user)
    context = {"title": "Notifications", "notifications": notifications}
    return render(request, "twits_notification.html", context)
