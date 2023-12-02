import pytest
from core.business_logic.services.twits_notifications import (
    adding_a_notification,
    get_user_notifications,
)
from core.models import Profiles, Twits


@pytest.mark.django_db
def test_adding_a_notification_successfully() -> None:
    twit = Twits.objects.get(text="test text twit_2")
    profile = Profiles.objects.get(username="testuser1")
    adding_a_notification(twit=twit, profile=profile)
    notifications = profile.notification.all()
    assert twit in notifications


@pytest.mark.django_db
def test_get_user_notifications_successfully() -> None:
    profile = Profiles.objects.get(username="testuser1")
    result = get_user_notifications(profile=profile)
    assert len(result) == 2
    assert result[0].created_at > result[1].created_at
