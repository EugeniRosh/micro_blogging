import pytest
from core.business_logic.services import deleting_a_twit_likes, like_a_twit
from core.models import Profiles, Twits


@pytest.mark.django_db
def test_like_a_twit_successfully() -> None:
    twit = Twits.objects.get(text="test text twit_2")
    profile = Profiles.objects.get(username="testuser3")
    result = like_a_twit(twit_id=twit.pk, profile=profile)
    assert result == "Like added"
    likes = twit.like.all()
    assert profile in likes


@pytest.mark.django_db
def test_like_a_twit_like_my_twit() -> None:
    twit = Twits.objects.get(text="test text twit_2")
    profile = Profiles.objects.get(username="testuser1")
    result = like_a_twit(twit_id=twit.pk, profile=profile)
    assert result == "You can't like your twit"
    likes = twit.like.all()
    assert profile not in likes


@pytest.mark.django_db
def test_deleting_a_twit_likes_successfully() -> None:
    twit = Twits.objects.get(text="test text twit_1")
    profile = Profiles.objects.get(username="testuser2")
    result = deleting_a_twit_likes(twit_id=twit.pk, profile=profile)
    assert result == "Like removed"
    likes = twit.like.all()
    assert profile not in likes


@pytest.mark.django_db
def test_deleting_a_twit_likes_remove_like_my_twit() -> None:
    twit = Twits.objects.get(text="test text twit_1")
    profile = Profiles.objects.get(username="testuser1")
    result = deleting_a_twit_likes(twit_id=twit.pk, profile=profile)
    assert result == "You can't delete likes on my twit"
