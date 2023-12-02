import pytest
from core.business_logic.exceptions import CreateUniqueError, GetValueError
from core.business_logic.services.profile import (
    add_follow,
    edit_profile,
    get_my_profile,
    get_profile,
    get_profile_by_username,
    get_profile_in_follow,
    get_user_profile,
    remove_follow,
)
from core.models import Profiles, Twits
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.http.request import QueryDict
from django.utils.datastructures import MultiValueDict


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


@pytest.mark.django_db
def test_edit_profile_succssefully() -> None:
    profile = Profiles.objects.get(username="testuser1")
    first_name_before_change = profile.first_name
    test_querydict = QueryDict("first_name=test_name")
    test_multivaluedict = MultiValueDict()
    edit_profile(
        username=profile.username, data=test_querydict, files=test_multivaluedict
    )
    profile.refresh_from_db()
    assert profile.first_name == "test_name"
    assert first_name_before_change != profile.first_name


@pytest.mark.django_db
def test_edit_profile_change_photo_succssefully(
    png_for_test: InMemoryUploadedFile,
) -> None:
    profile = Profiles.objects.get(username="testuser1")
    photo_before_change = profile.photo
    test_querydict = QueryDict()
    test_multivaluedict = MultiValueDict({"photo": [png_for_test]})
    edit_profile(
        username=profile.username, data=test_querydict, files=test_multivaluedict
    )
    profile.refresh_from_db()
    name_photo_test = str(profile.photo).split("/")[-1]
    assert name_photo_test == png_for_test.name
    assert profile.photo != photo_before_change


@pytest.mark.django_db
def test_edit_profile_change_email_succssefully() -> None:
    profile = Profiles.objects.get(username="testuser1")
    email_before_change = profile.email
    test_querydict = QueryDict("email=testemail@gmail.com")
    test_multivaluedict = MultiValueDict()
    edit_profile(
        username=profile.username, data=test_querydict, files=test_multivaluedict
    )
    profile.refresh_from_db()
    assert profile.email == "testemail@gmail.com"
    assert profile.email != email_before_change
    assert profile.is_active is False


@pytest.mark.django_db
def test_edit_profile_raise_createuniqueerror() -> None:
    test_querydict = QueryDict("email=testuser2@gmail.com")
    test_multivaluedict = MultiValueDict()
    with pytest.raises(CreateUniqueError):
        edit_profile(
            username="testuser1", data=test_querydict, files=test_multivaluedict
        )


@pytest.mark.django_db
def test_add_follow_succssefully() -> None:
    profile = Profiles.objects.get(username="testuser3")
    user_following = Profiles.objects.get(username="testuser2")
    add_follow(user=profile, user_following=user_following.username)
    profile.refresh_from_db()
    following = profile.followers.all()
    assert len(following) == 1
    assert user_following in following


@pytest.mark.django_db
def test_add_follow_createuniqueerror() -> None:
    profile = Profiles.objects.get(username="testuser3")
    user_following = "testuser999"
    with pytest.raises(GetValueError):
        add_follow(user=profile, user_following=user_following)


@pytest.mark.django_db
def test_remove_follow_succssefully() -> None:
    profile = Profiles.objects.get(username="testuser1")
    user_following = Profiles.objects.get(username="testuser2")
    remove_follow(user=profile, user_following=user_following.username)
    profile.refresh_from_db()
    following = profile.followers.all()
    assert len(following) == 1
    assert user_following not in following


@pytest.mark.django_db
def test_remove_follow_createuniqueerror() -> None:
    profile = Profiles.objects.get(username="testuser3")
    user_following = "testuser999"
    with pytest.raises(GetValueError):
        remove_follow(user=profile, user_following=user_following)


@pytest.mark.django_db
def test_get_profile_in_follow_succssefully() -> None:
    profile_1 = Profiles.objects.get(username="testuser2")
    profile_2 = Profiles.objects.get(username="testuser1")
    follow_true = get_profile_in_follow(profile=profile_1, profile_follow=profile_2)
    assert type(follow_true) == bool
    assert follow_true is True
    profile_3 = Profiles.objects.get(username="testuser3")
    follow_false = get_profile_in_follow(profile=profile_1, profile_follow=profile_3)
    assert type(follow_true) == bool
    assert follow_false is False
