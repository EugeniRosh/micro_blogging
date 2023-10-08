from __future__ import annotations

from typing import TYPE_CHECKING

from core.models import Twits, TwitsProfilesNotifications
from django.db.models import Q

if TYPE_CHECKING:
    from core.models import Profiles
    from django.db.models.query import QuerySet


def adding_a_notification(profile: Profiles, twit: Twits) -> None:
    profile.notification.add(twit)
    return None


def get_user_notifications(profile: Profiles) -> QuerySet:
    notifications = (
        TwitsProfilesNotifications.objects.filter(
            Q(twit__profile=profile) | Q(twit__profile__is_staff=True, profile=profile)
        )
        .prefetch_related("twit", "profile", "twit__profile")
        .order_by("-created_at")
    )

    return list(notifications)
