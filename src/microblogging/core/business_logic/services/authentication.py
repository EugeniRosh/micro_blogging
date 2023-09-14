from __future__ import annotations

import logging
from typing import TYPE_CHECKING

from core.business_logic.exceptions import GetValueError
from django.contrib.auth import authenticate, login, logout

if TYPE_CHECKING:
    from core.business_logic.dto import AuthenticationDTO
    from django.http import HttpRequest

logger = logging.getLogger(__name__)


def authentication_user(request: HttpRequest, data: AuthenticationDTO) -> None:
    user = authenticate(request=request, email=data.email, password=data.password)
    if user:
        logger.info(f"User {data.email} is logged in")
        login(request=request, user=user)
    else:
        raise GetValueError

    return None


def logout_user(request: HttpRequest) -> None:
    logout(request=request)
    return None
