from __future__ import annotations

from typing import TYPE_CHECKING

from .twits import get_twit_by_id
from .twits_notifications import adding_a_notification

if TYPE_CHECKING:
    from core.models import Profiles, Twits


def like_a_twit(twit_id: int, profile: Profiles) -> str:
    twit: Twits = get_twit_by_id(twit_id=twit_id)

    if twit.profile == profile:
        return "you can't like your twit"

    twit.like.add(profile)
    adding_a_notification(profile=profile, twit=twit)
    return "like added"


def deleting_a_twit_likes(twit_id: int, profile: Profiles) -> str:
    twit: Twits = get_twit_by_id(twit_id=twit_id)

    if twit.profile == profile:
        return "You can't delete likes on my twit"

    twit.like.remove(profile)
    return "like removed"
