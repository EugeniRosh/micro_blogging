import pytest
from core.business_logic.exceptions import GetValueError
from core.business_logic.services.profile import get_profile, get_profile_by_username
from core.models import Profiles, Twits


@pytest.mark.django_db
def test_get_profile_by_username_succssefully() -> None:
    profile = Profiles.objects.get(username="testuser1")
    test_profile = get_profile_by_username(username=profile.username)
    assert profile == test_profile


@pytest.mark.django_db
def test_get_profile_by_username_raise_getvalueerror() -> None:
    with pytest.raises(GetValueError):
        get_profile_by_username(username="does_not_exist")


@pytest.mark.django_db
def test_get_profile_succssefully() -> None:
    profile = Profiles.objects.get(username="testuser1")
    test_profile, test_twits, test_follow = get_profile(username=profile.username)
    assert test_profile == profile
    assert type(test_follow) == bool
    assert test_follow is False
    assert type(test_twits) == list
    assert type(test_twits[0]) == Twits


@pytest.mark.django_db
def test_get_profile_raise_getvalueerror() -> None:
    with pytest.raises(GetValueError):
        get_profile(username="does_not_exist")
