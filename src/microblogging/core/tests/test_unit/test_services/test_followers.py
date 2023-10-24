import pytest
from core.business_logic.services import get_all_followers, get_all_following
from django.db.models.query import QuerySet


@pytest.mark.django_db
def test_get_all_followers_successfully() -> None:
    followers = get_all_followers(username="testuser1")
    assert type(followers) == QuerySet
    assert len(followers) == 1
    assert followers[0]["follower__username"] == "testuser2"


@pytest.mark.django_db
def test_get_all_followers_non_existing_user() -> None:
    followers = get_all_followers(username="qwerty")
    assert len(followers) == 0
    assert list(followers) == []


@pytest.mark.django_db
def test_get_all_following_successfully() -> None:
    followers = get_all_following(username="testuser1")
    assert type(followers) == QuerySet
    assert len(followers) == 2
    assert followers[0]["following__username"] == "testuser2"


@pytest.mark.django_db
def test_get_all_following_non_existing_user() -> None:
    followers = get_all_following(username="qwerty")
    assert len(followers) == 0
    assert list(followers) == []
