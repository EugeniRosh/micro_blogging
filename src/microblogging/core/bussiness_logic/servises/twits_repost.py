from __future__ import annotations

from typing import TYPE_CHECKING

from .twits import get_tweet_by_id

if TYPE_CHECKING:
    from core.models import Profiles, Twits


def add_repost_twits(twit_id: int, profile: Profiles) -> None:
    twit: Twits = get_tweet_by_id(twit_id=twit_id)

    twit.repost.add(profile)
    return None


def delete_repost_twits(twit_id: int, profile: Profiles) -> None:
    twit: Twits = get_tweet_by_id(twit_id=twit_id)

    twit.repost.remove(profile)
    return None
