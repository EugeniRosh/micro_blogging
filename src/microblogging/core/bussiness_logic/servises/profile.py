from __future__ import annotations

import logging
from typing import TYPE_CHECKING

from core.bussiness_logic.exeptions import CreateUniqueError, GetValueError
from core.models import Profiles
from django.db.models import Count
from django.db.utils import IntegrityError

from .common import change_photo

if TYPE_CHECKING:
    from django.db.models.query import QuerySet
    from django.http.request import QueryDict
    from django.utils.datastructures import MultiValueDict

logger = logging.getLogger(__name__)


def get_user_profile(username: str) -> QuerySet:
    try:
        profile = Profiles.objects.annotate(
            count_followers=Count("user_following", distinct=True),
            count_following=Count("user_follower", distinct=True),
        ).get(username=username)
    except Profiles.DoesNotExist:
        raise GetValueError

    logger.info(f"Get info user: {username}")
    return profile


def edit_profile(username: str, data: QueryDict, files: MultiValueDict) -> None:
    if "photo" in files:
        data = change_photo(field="photo", data=files)

    try:
        Profiles.objects.update_or_create(username=username, defaults=data)
        logger.info(f"Profile edit. username: {username}. {data}")
    except IntegrityError as err:
        raise CreateUniqueError(err)

    return None
