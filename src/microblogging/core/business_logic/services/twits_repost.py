from __future__ import annotations

from typing import TYPE_CHECKING

from .twits import get_twit_by_id

if TYPE_CHECKING:
    from core.models import Profiles, Twits


def repost_the_twit(twit_id: int, profile: Profiles) -> None:
    twit: Twits = get_twit_by_id(twit_id=twit_id)

    if twit.profile == profile:
        return None

    twit.repost.add(profile)
    return None


def delete_repost_twits(twit_id: int, profile: Profiles) -> None:
    twit: Twits = get_twit_by_id(twit_id=twit_id)

    if twit.profile == profile:
        return None

    twit.repost.remove(profile)
    return None
