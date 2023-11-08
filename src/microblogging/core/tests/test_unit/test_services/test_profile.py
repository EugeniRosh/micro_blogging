import pytest
from core.business_logic.exceptions import GetValueError
from core.business_logic.services.profile import (
    get_my_profile,
    get_profile,
    get_profile_by_username,
    get_user_profile,
)
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
    assert len(test_twits) == 6
    assert test_twits[0].created_at > test_twits[1].created_at


@pytest.mark.django_db
def test_get_profile_raise_getvalueerror() -> None:
    with pytest.raises(GetValueError):
        get_profile(username="does_not_exist")


@pytest.mark.django_db
def test_get_my_profile_succssefully() -> None:
    profile = Profiles.objects.get(username="testuser1")
    test_user_profile, test_twits = get_my_profile(profile=profile)
    assert test_user_profile == profile
    assert test_user_profile.count_followers == 1
    assert test_user_profile.count_following == 2

    assert type(test_twits) == list
    assert type(test_twits[0]) == Twits
    assert len(test_twits) == 6
    assert test_twits[0].created_at > test_twits[1].created_at


@pytest.mark.django_db
def test_get_my_profile_getvalueerror() -> None:
    profile = Profiles(username="does_not_exist")
    with pytest.raises(GetValueError):
        get_my_profile(profile=profile)


@pytest.mark.django_db
def test_get_user_profile_succssefully() -> None:
    profile = Profiles.objects.get(username="testuser1")
    test_profile = get_user_profile(username=profile.username)

    assert test_profile == profile
    assert test_profile.count_followers == 1
    assert test_profile.count_following == 2


@pytest.mark.django_db
def test_get_user_profile_getvalueerror() -> None:
    with pytest.raises(GetValueError):
        get_profile(username="does_not_exist")
