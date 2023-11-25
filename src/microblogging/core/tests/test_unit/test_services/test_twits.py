import pytest
from core.business_logic.exceptions import GetValueError
from core.business_logic.services.twits import (
    get_repost_twit,
    get_twit_by_id,
    get_twits,
    get_twits_and_counts_of_likes_of_reposts_of_answer,
    get_twits_and_reposts,
)
from core.models import Profiles, Twits
from django.db.models.query import QuerySet


@pytest.mark.django_db
def test_get_twits_and_counts_of_likes_of_reposts_of_answer_succssefully() -> None:
    twits = get_twits_and_counts_of_likes_of_reposts_of_answer()
    assert type(twits) == QuerySet
    twit = twits[0]
    assert type(twit) == Twits
    assert type(twit.count_like) == int
    assert type(twit.count_repost) == int
    assert type(twit.count_answer) == int


@pytest.mark.django_db
def test_get_twit_by_id_succssefully() -> None:
    twits = Twits.objects.all()
    twit = twits[0]
    twit_test = get_twit_by_id(twit_id=twit.pk)
    assert type(twit_test) == Twits
    assert twit == twit_test


@pytest.mark.django_db
def test_get_twit_by_id_raise_getvalueerror() -> None:
    twits = Twits.objects.all()
    twit_id_for_test = list(twits)[-1].pk + 1
    with pytest.raises(GetValueError):
        get_twit_by_id(twit_id=twit_id_for_test)


@pytest.mark.django_db
def test_get_repost_twit_succssefully() -> None:
    profile = Profiles.objects.get(username="testuser1")
    twits = get_repost_twit(profile=profile)
    assert type(twits) == QuerySet
    assert type(twits[0]) == Twits
    assert len(twits) == 3


@pytest.mark.django_db
def test_get_twits_and_reposts_succssefully() -> None:
    profile = Profiles.objects.get(username="testuser1")
    twits = get_twits_and_reposts(profile=profile)
    assert type(twits) == list
    assert type(twits[0]) == Twits
    assert len(twits) == 6
    assert twits[0].created_at > twits[1].created_at


@pytest.mark.django_db
def test_get_twits_succssefully() -> None:
    profile = Profiles.objects.get(username="testuser1")
    twits = Twits.objects.filter(profile=profile)
    twits_for_test = get_twits(twits_list=twits, profile=profile)
    assert type(twits_for_test) == QuerySet
    assert type(twits_for_test[0]) == Twits
    assert len(twits_for_test) == 3
    assert twits_for_test[0].created_at > twits_for_test[1].created_at
