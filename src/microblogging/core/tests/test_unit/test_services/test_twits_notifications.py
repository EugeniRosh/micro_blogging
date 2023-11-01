import pytest
from core.business_logic.services.twits_notifications import adding_a_notification
from core.models import Profiles, Twits


@pytest.mark.django_db
def test_adding_a_notification_successfully() -> None:
    twit = Twits.objects.get(text="test text twit_2")
    profile = Profiles.objects.get(username="testuser1")
    adding_a_notification(twit=twit, profile=profile)
    notifications = profile.notification.all()
    assert twit in notifications
