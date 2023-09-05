from __future__ import annotations

import logging
from time import time
from typing import TYPE_CHECKING
from uuid import uuid4

from core.models import EmailConfirmationCode
from django.conf import settings
from django.core.mail import send_mail
from django.urls import reverse

if TYPE_CHECKING:
    from core.models import Profiles

logger = logging.getLogger(__name__)


def send_confirmation_code(user: Profiles, email: str) -> None:
    confirmation_code = uuid4()
    EmailConfirmationCode.objects.create(
        code=confirmation_code,
        profile=user,
        expiration=settings.CONFIRMATION_CODE_LIFE_TIME + int(time()),
    )
    confirmation_url = (
        settings.SERVER_HOST + reverse("confirm_signup") + f"?code={confirmation_code}"
    )
    send_mail(
        subject="Confirm your email",
        message=f"Please confirm email by clicking the link below:\n\n{confirmation_url}",
        from_email=settings.DEFAULT_EMAIL_FROM,
        recipient_list=[email],
    )

    logger.info(f"Confirmation code sent. email:{email}. code:{confirmation_code}")
    return None
