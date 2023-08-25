from __future__ import annotations

import logging
from time import time
from typing import TYPE_CHECKING
from uuid import uuid4

from core.bussiness_logic.exeptions import (
    CreateUniqueError,
    ExpirationTimeError,
    GetValueError,
)
from core.models import EmailConfirmationCode
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import Group
from django.db.utils import IntegrityError

if TYPE_CHECKING:
    from core.bussiness_logic.dto import RegistrationDTO
    from core.models import Profiles

logger = logging.getLogger(__name__)


def regisration_user(data: RegistrationDTO) -> None:
    user_model = get_user_model()
    try:
        data.password = make_password(data.password)
        create_user = user_model.objects.create(
            username=data.username,
            email=data.email,
            date_of_birth=data.date_of_birth,
            is_active=False,
            password=data.password,
        )

    except IntegrityError as err:
        raise CreateUniqueError(err)

    role = Group.objects.get(name=data.role)
    create_user.groups.add(role)

    logger.info(f"Created user:{data.username}")

    confirmation_code = uuid4()
    EmailConfirmationCode.objects.create(
        code=confirmation_code,
        profile=create_user,
        expiration=settings.CONFIRMATION_CODE_LIFE_TIME + int(time()),
    )

    registration_confirmations(confirmation_code=str(confirmation_code))
    logger.info(f"Confirmation code sent. email:{data.email}. code:{confirmation_code}")

    return None


def registration_confirmations(confirmation_code: str) -> None:
    try:
        email_confirmation_code = EmailConfirmationCode.objects.get(
            code=confirmation_code
        )
    except EmailConfirmationCode.DoesNotExist:
        logger.error(f"Confirmation code does not exist. code:{confirmation_code}")
        raise GetValueError

    confirmation_time = int(time())

    if email_confirmation_code.expiration < confirmation_time:
        logger.error(
            f"Expired confirmation code. code:{confirmation_code}. time:{confirmation_time}"
        )
        raise ExpirationTimeError

    user: Profiles = email_confirmation_code.profile
    user.is_active = True
    user.save()
    logger.info(f"User activated. username:{user.username}")

    email_confirmation_code.delete()

    return None
