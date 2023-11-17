from __future__ import annotations

import logging
from typing import TYPE_CHECKING

from core.models import Followers

if TYPE_CHECKING:
    from django.db.models.query import QuerySet

logger = logging.getLogger(__name__)


def get_all_followers(username: str) -> QuerySet[Followers]:
    followers = (
        Followers.objects.prefetch_related("profiles")
        .values("follower__username")
        .filter(following__username=username)
    )

    logger.info(f"Get user followers. user: {username}")
    return followers


def get_all_following(username: str) -> QuerySet[Followers]:
    following = (
        Followers.objects.prefetch_related("profiles")
        .values("following__username")
        .filter(follower__username=username)
    )

    logger.info(f"Get user following. user: {username}")
    return following
