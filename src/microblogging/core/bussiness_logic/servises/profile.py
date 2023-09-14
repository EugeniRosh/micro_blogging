from __future__ import annotations

import logging
from typing import TYPE_CHECKING

from core.bussiness_logic.exeptions import CreateUniqueError, GetValueError
from core.models import Profiles
from django.db.models import Count
from django.db.utils import IntegrityError

from .common import change_photo
from .send_mail import send_confirmation_code
from .twits import get_repost_twit, get_twits

if TYPE_CHECKING:
    from django.db.models.query import QuerySet
    from django.http.request import QueryDict
    from django.utils.datastructures import MultiValueDict

logger = logging.getLogger(__name__)


def get_profile_by_username(username: str) -> Profiles:
    try:
        profile: Profiles = Profiles.objects.get(username=username)
    except Profiles.DoesNotExist:
        raise GetValueError

    return profile


def get_profile(username: str) -> tuple[Profiles, QuerySet]:
    profile = get_user_profile(username=username)
    repost_twits = get_repost_twit(profile=profile)
    twits = get_twits(twits_list=repost_twits, profile=profile)
    return profile, twits


def get_user_profile(username: str) -> Profiles:
    try:
        profile: Profiles = Profiles.objects.annotate(
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
    elif "email" in data:
        profile, profile_bool = Profiles.objects.update_or_create(
            username=username, defaults={"is_active": False}
        )
        send_confirmation_code(user=profile, email=data["email"])

    try:
        Profiles.objects.update_or_create(username=username, defaults=data)
        logger.info(f"Profile edit. username: {username}. {data}")
    except IntegrityError as err:
        raise CreateUniqueError(err)

    return None


def add_follow(user: Profiles, user_following: str) -> None:
    user_following_db = get_profile_by_username(username=user_following)

    user.followers.add(user_following_db)
    return None


def remove_follow(user: Profiles, user_following: str) -> None:
    user_following_db = get_profile_by_username(username=user_following)

    user.followers.remove(user_following_db)
    return None


def get_profile_in_follow(profile: Profiles, profile_follow: Profiles) -> bool:
    follow: bool = profile.followers.filter(pk=profile_follow.pk).exists()
    return follow
