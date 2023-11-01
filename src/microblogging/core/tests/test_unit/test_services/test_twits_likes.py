import pytest
from core.business_logic.services import like_a_twit
from core.models import Profiles, Twits


@pytest.mark.django_db
def test_like_a_twit_successfully() -> None:
    twit = Twits.objects.get(text="test text twit_2")
    profile = Profiles.objects.get(username="testuser3")
    result = like_a_twit(twit_id=twit.pk, profile=profile)
    assert result == "like added"
    likes = twit.like.all()
    assert profile in likes


@pytest.mark.django_db
def test_like_a_twit_like_my_tweet() -> None:
    twit = Twits.objects.get(text="test text twit_2")
    profile = Profiles.objects.get(username="testuser1")
    result = like_a_twit(twit_id=twit.pk, profile=profile)
    assert result == "you can't like your tweet"
    likes = twit.like.all()
    assert profile not in likes
