import pytest
from core.business_logic.exceptions import GetValueError
from core.business_logic.services.profile import get_profile_by_username
from core.models import Profiles


@pytest.mark.django_db
def test_get_profile_by_username_succssefully() -> None:
    profile = Profiles.objects.get(username="testuser1")
    test_profile = get_profile_by_username(username=profile.username)
    assert profile == test_profile


@pytest.mark.django_db
def test_get_profile_by_username_raise_getvalueerror() -> None:
    with pytest.raises(GetValueError):
        get_profile_by_username(username="does_not_exist")
