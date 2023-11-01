import pytest
from core.business_logic.services import repost_the_twit
from core.models import Profiles, Twits


@pytest.mark.django_db
def test_repost_the_twit_successfully() -> None:
    twit = Twits.objects.get(text="test text twit_3")
    profile = Profiles.objects.get(username="testuser2")
    result = repost_the_twit(twit_id=twit.pk, profile=profile)
    assert result == "Repost added"
    reposts = twit.repost.all()
    assert profile in reposts


@pytest.mark.django_db
def test_repost_the_twit_repost_my_twit() -> None:
    twit = Twits.objects.get(text="test text twit_2")
    profile = Profiles.objects.get(username="testuser1")
    result = repost_the_twit(twit_id=twit.pk, profile=profile)
    assert result == "You can't repost your twit"
    reposts = twit.repost.all()
    assert profile not in reposts
