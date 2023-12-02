import pytest
from core.business_logic.services import delete_repost_twits, repost_the_twit
from core.models import Profiles, Twits


@pytest.mark.django_db
def test_repost_the_twit_successfully() -> None:
    twit = Twits.objects.get(text="test text twit_3")
    profile = Profiles.objects.get(username="testuser2")
    assert profile not in twit.repost.all()
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


@pytest.mark.django_db
def test_delete_repost_twits_reposts_successfully() -> None:
    twit = Twits.objects.get(text="test text twit_1")
    profile = Profiles.objects.get(username="testuser2")
    assert profile in twit.repost.all()
    result = delete_repost_twits(twit_id=twit.pk, profile=profile)
    assert result == "Repost removed"
    reposts = twit.repost.all()
    assert profile not in reposts


@pytest.mark.django_db
def test_delete_repost_twits_remove_repost_my_twit() -> None:
    twit = Twits.objects.get(text="test text twit_1")
    profile = Profiles.objects.get(username="testuser1")
    result = delete_repost_twits(twit_id=twit.pk, profile=profile)
    assert result == "You can't delete repost on my twit"
