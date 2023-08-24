from __future__ import annotations

import logging
from typing import TYPE_CHECKING

from core.models import Profiles, Twits
from django.db.models import Count, Q

if TYPE_CHECKING:
    from django.db.models.query import QuerySet


logger = logging.getLogger(__name__)


def get_twits_reposts(profile: str) -> QuerySet:
    repost_twits = Twits.objects.prefetch_related("repost").filter(repost=profile)

    return repost_twits


def get_twits(twits_list: QuerySet, profile: Profiles) -> QuerySet:
    twits = (
        Twits.objects.select_related("profile")
        .prefetch_related("like", "repost")
        .annotate(
            count_like=Count("like", distinct=True),
            count_repost=Count("repost", distinct=True),
            count_answer=Count("answer_to_twit", distinct=True),
        )
        .filter(Q(profile=profile) | Q(id__in=twits_list))
        .order_by("-created_at")
    )
    return twits
