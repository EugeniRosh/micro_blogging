from __future__ import annotations

import logging
from typing import TYPE_CHECKING

from core.business_logic.exceptions import GetValueError, ProfileAccessError
from core.models import Profiles, Twits
from django.db.models import Count, Q

from .tags import get_a_tag_to_search_for_tweets, get_tags

if TYPE_CHECKING:
    from core.business_logic.dto import TagsSearchDTO, TwitsDTO
    from core.models import Tags
    from django.db.models.query import QuerySet

logger = logging.getLogger(__name__)


def get_twits_and_counts_of_likes_of_reposts_of_answer() -> QuerySet[Twits]:
    twits = (
        Twits.objects.select_related("profile", "answer_to_twit")
        .prefetch_related("like", "repost")
        .annotate(
            count_like=Count("like", distinct=True),
            count_repost=Count("repost", distinct=True),
            count_answer=Count("answer", distinct=True),
        )
    )
    return twits


def get_twit_by_id(twit_id: int) -> Twits:
    try:
        twit: Twits = Twits.objects.select_related("profile", "answer_to_twit").get(
            id=twit_id
        )
    except Twits.DoesNotExist:
        raise GetValueError

    return twit


def get_repost_twit(profile: Profiles) -> QuerySet[Twits]:
    repost_twits = Twits.objects.filter(repost=profile)
    logger.info(f"Get twits repost. profile: {profile.id}")
    return repost_twits


def get_twits_and_reposts(profile: Profiles) -> list[Twits]:
    repost_twits = get_repost_twit(profile=profile)
    twits = get_twits(twits_list=repost_twits, profile=profile)
    return list(twits)


def get_twits(twits_list: QuerySet[Twits], profile: Profiles) -> QuerySet[Twits]:
    twits = get_twits_and_counts_of_likes_of_reposts_of_answer()

    twits = twits.filter(Q(profile=profile) | Q(id__in=twits_list)).order_by(
        "-created_at"
    )

    logger.info(f"Get twits and repost twits. profile: {profile.id}")
    return twits


def add_a_twits(data: TwitsDTO, profile: Profiles) -> Twits:
    tags = get_tags(tags=data.tag)

    twit_db: Twits = Twits.objects.create(text=data.text, profile=profile)

    twit_db.tag.set(tags)
    logger.info(f"Create twit. twit: {twit_db.id}")
    return twit_db


def get_tweet_for_viewing(
    twit_id: int, profile: Profiles
) -> tuple[Twits, list[Tags], list[Twits], bool | None, bool | None]:
    try:
        twit, tags, twits_ansver = view_twits(twit_id=twit_id)
    except GetValueError:
        raise GetValueError

    if profile != twit.profile:
        like_twit = get_profile_like_on_twit(profile=profile, twit=twit)
        repost_twit = get_profile_repost_on_twit(profile=profile, twit=twit)
    else:
        like_twit = None
        repost_twit = None

    logger.info(f"Get twit for viewing. twit: {twit.id}")
    return twit, tags, twits_ansver, like_twit, repost_twit


def view_twits(twit_id: int) -> tuple[Twits, list[Tags], list[Twits]]:
    try:
        twit: Twits = get_twit_by_id(twit_id=twit_id)
    except Twits.DoesNotExist:
        raise GetValueError

    twits_ansver = Twits.objects.filter(answer_to_twit=twit)

    tag = twit.tag.all()

    logger.info(f"Get info twit. twit: {twit.id}")

    return twit, list(tag), list(twits_ansver)


def delete_twits(twit_id: int, profile: Profiles) -> None:
    twit: Twits = get_twit_by_id(twit_id=twit_id)

    if twit.profile != profile:
        raise ProfileAccessError

    twit.delete()

    return None


def get_profile_like_on_twit(profile: Profiles, twit: Twits) -> bool:
    like_twit: bool = twit.like.filter(pk=profile.pk).exists()
    logger.info(f"Got a like. twit: {twit.id}. profile: {profile.id}")
    return like_twit


def get_profile_repost_on_twit(profile: Profiles, twit: Twits) -> bool:
    repost_twit: bool = twit.repost.filter(pk=profile.pk).exists()
    logger.info(f"Got a repost. twit: {twit.id}. profile: {profile.id}")
    return repost_twit


def creat_answer_to_twit(twit_id: int, data: TwitsDTO, profile: Profiles) -> None:
    twit = get_twit_by_id(twit_id=twit_id)

    tags = get_tags(tags=data.tag)

    twit_answer = Twits.objects.create(
        text=data.text, answer_to_twit=twit, profile=profile
    )

    twit_answer.tag.set(tags)
    logger.info(f"Created a answer to the twit. twit: {twit.id}.")
    return None


def get_info_twit_for_edit(twit_id: int) -> tuple[Twits, list[Tags]]:
    twit: Twits = get_twit_by_id(twit_id=twit_id)

    tags = twit.tag.all()
    return twit, list(tags)


def edit_twit(twit_db: Twits, data: TwitsDTO) -> None:
    twit_db.text = data.text
    twit_db.save()

    tags = get_tags(tags=data.tag)
    twit_db.tag.set(tags)

    logger.info(f"Twit from edited. twit: {twit_db.id}.")
    return None


def get_twits_to_index_page(profile: Profiles, sort_string: str) -> list[Twits]:
    followers = profile.followers.all()
    reposted_tweets_from_followers = Twits.objects.filter(repost__in=followers)

    twits = get_twits_and_counts_of_likes_of_reposts_of_answer()
    twits = twits.filter(
        Q(profile=profile)
        | Q(repost=profile)
        | Q(profile__in=followers)
        | Q(id__in=reposted_tweets_from_followers)
    ).order_by(f"-{sort_string}")

    logger.info(
        f"Received twits for home page. profile: {profile.id}. sort_string: {sort_string}"
    )
    return list(twits)


def get_twits_by_tag(data: TagsSearchDTO) -> list[Twits]:
    search_tag = get_a_tag_to_search_for_tweets(tag=data.tag)

    twits = get_twits_and_counts_of_likes_of_reposts_of_answer()

    twits = twits.filter(tag__in=search_tag).order_by("-created_at")

    logger.info(f"Received twits by tag. tag: {data.tag}.")
    return list(twits)
