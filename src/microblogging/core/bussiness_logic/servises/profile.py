from __future__ import annotations

import logging

from core.bussiness_logic.exeptions import GetValueError
from core.models import Profiles
from django.db.models import Count

logger = logging.getLogger(__name__)


def get_user_profile(username: str) -> list[Profiles]:
    profile = (
        Profiles.objects.prefetch_related("notification", "followers")
        .annotate(
            count_followers=Count("followers__follower_profile"),
            count_following=Count("followers__follower"),
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
        .filter(username=username)
    )
    if not profile:
        raise GetValueError

    logger.info(f"Get info user: {username}")
    return list(profile)
