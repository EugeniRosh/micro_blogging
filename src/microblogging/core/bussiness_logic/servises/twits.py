from __future__ import annotations

import logging
from typing import TYPE_CHECKING

from core.bussiness_logic.exeptions import GetValueError
from core.models import Profiles, Tags, Twits
from django.db.models import Count, Q

from .tags import get_tegs

if TYPE_CHECKING:
    from core.bussiness_logic.dto import TwitsDTO
    from django.db.models.query import QuerySet


logger = logging.getLogger(__name__)


def get_twits_reposts(profile: Profiles) -> QuerySet:
    repost_twits = Twits.objects.prefetch_related("repost").filter(repost=profile)
    logger.info(f"Get twits repost. profile: {profile.id}")
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
    logger.info(f"Get twits and repost twits. profile: {profile.id}")
    return twits


def add_twits(data: TwitsDTO, profile: Profiles) -> None:
    tags = get_tegs(tags=data.tag)

    twits_db = Twits.objects.create(text=data.text, profile=profile)

    twits_db.tag.set(tags)
    logger.info(f"Create twit. twit: {twits_db.id}")
    return None


def view_twits(twit_id: int) -> tuple[Twits, list[Tags]]:
    try:
        twit = (
            Twits.objects.select_related("profile")
            .prefetch_related("tag")
            .get(id=twit_id)
        )
    except Twits.DoesNotExist:
        raise GetValueError

    tag = twit.tag.all()
    logger.info(f"Get info twit. twit: {twit.id}")
    return twit, list(tag)
