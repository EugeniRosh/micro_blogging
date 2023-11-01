from __future__ import annotations

from typing import TYPE_CHECKING

from .twits import get_twit_by_id

if TYPE_CHECKING:
    from core.models import Profiles, Twits


def repost_the_twit(twit_id: int, profile: Profiles) -> str:
    twit: Twits = get_twit_by_id(twit_id=twit_id)

    if twit.profile == profile:
        return "You can't repost your twit"

    twit.repost.add(profile)
    return "Repost added"


def delete_repost_twits(twit_id: int, profile: Profiles) -> str:
    twit: Twits = get_twit_by_id(twit_id=twit_id)

    if twit.profile == profile:
        return "You can't delete repost on my twit"

    twit.repost.remove(profile)
    return "Repost removed"
