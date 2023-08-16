from __future__ import annotations

import logging

from core.bussiness_logic.dto import CountFollowersProfileDTO, ProfileDTO
from core.bussiness_logic.exeptions import GetValueError
from core.models import Profiles
from django.db.models import Count

from .common import convert_data_from_form_in_dacite

logger = logging.getLogger(__name__)


def get_user_profile(username: str) -> tuple[ProfileDTO, CountFollowersProfileDTO]:
    profile = (
        Profiles.objects.annotate(
            count_followers=Count("user_following", distinct=True),
            count_following=Count("user_follower", distinct=True),
        )
        .values(
            "username",
            "photo",
            "first_name",
            "last_name",
            "date_joined",
            "country",
            "description",
            "count_followers",
            "count_following",
        )
        .get(username=username)
    )

    if not profile:
        raise GetValueError
    profile_dto = convert_data_from_form_in_dacite(dto=ProfileDTO, data=profile)
    counter_followers = convert_data_from_form_in_dacite(
        dto=CountFollowersProfileDTO, data=profile
    )

    logger.info(f"Get info user: {username}")
    return profile_dto, counter_followers
