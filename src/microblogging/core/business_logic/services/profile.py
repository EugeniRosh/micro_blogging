from __future__ import annotations

import logging
from typing import TYPE_CHECKING

from core.business_logic.exceptions import CreateUniqueError, GetValueError
from core.models import Profiles
from django.db.models import Count
from django.db.utils import IntegrityError

from .common import change_photo
from .send_an_mail import send_confirmation_code
from .twits import get_twits_and_reposts

if TYPE_CHECKING:
    from core.models import Twits
    from django.http.request import QueryDict
    from django.utils.datastructures import MultiValueDict

logger = logging.getLogger(__name__)


def get_profile_by_username(username: str) -> Profiles:
    try:
        profile: Profiles = Profiles.objects.get(username=username)
    except Profiles.DoesNotExist:
        raise GetValueError

    return profile


def get_profile(username: str) -> tuple[Profiles, list[Twits], bool]:
    profile = get_user_profile(username=username)
    twits = get_twits_and_reposts(profile=profile)
    follow = get_profile_in_follow(profile=profile, profile_follow=profile)

    logger.info(f"Get info user. username: {username}")
    return profile, twits, follow


def get_my_profile(profile: Profiles) -> tuple[Profiles, list[Twits]]:
    user_profile = get_user_profile(username=profile.username)
    twits = get_twits_and_reposts(profile=profile)

    logger.info(f"Get info user. profile: {profile.id}")
    return user_profile, twits


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

    try:
        Profiles.objects.update_or_create(username=username, defaults=data)
        logger.info(f"Profile edit. username: {username}. {data}")
    except IntegrityError as err:
        raise CreateUniqueError(err)

    if "email" in data:
        profile, profile_bool = Profiles.objects.update_or_create(
            username=username, defaults={"is_active": False}
        )
        send_confirmation_code(user=profile, email=data["email"])

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

    logger.info(f"Got a follow. profile: {profile.id}")
    return follow
