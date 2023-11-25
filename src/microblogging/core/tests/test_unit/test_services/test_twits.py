import pytest
from core.business_logic.dto import TwitsDTO
from core.business_logic.exceptions import GetValueError
from core.business_logic.services.twits import (
    add_a_twits,
    get_repost_twit,
    get_tweet_for_viewing,
    get_twit_by_id,
    get_twits,
    get_twits_and_counts_of_likes_of_reposts_of_answer,
    get_twits_and_reposts,
    view_twits,
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


@pytest.mark.django_db
def test_add_a_twits_succssefully() -> None:
    profile = Profiles.objects.get(username="testuser1")
    twit_dto = TwitsDTO(
        text="test add a twits succssefully", tag="pyton\r\ntest\r\ntwits"
    )
    twit_db = add_a_twits(data=twit_dto, profile=profile)
    assert type(twit_db) == Twits
    assert twit_db.text == "test add a twits succssefully"
    assert twit_db.profile == profile
    tags = twit_db.tag.all()
    assert len(tags) == 3
    for tag in tags:
        assert tag.tag in ["pyton", "test", "twits"]


@pytest.mark.django_db
def test_get_tweet_for_viewing_my_twit_succssefully() -> None:
    twit_from_db = Twits.objects.get(text="test text twit_2")
    tags_db = twit_from_db.tag.all()
    profile = twit_from_db.profile
    twit, tags, twits_ansver, like_twit, repost_twit = get_tweet_for_viewing(
        twit_id=twit_from_db.pk, profile=profile
    )
    assert twit == twit_from_db
    assert list(tags_db) == tags
    assert type(twits_ansver) == list
    assert len(twits_ansver) == 1
    assert type(twits_ansver[0]) == Twits
    assert twits_ansver[0].text == "test text twit_5"
    assert like_twit is None
    assert repost_twit is None


@pytest.mark.django_db
def test_get_tweet_for_viewing_someone_else_twit_succssefully() -> None:
    twit_from_db = Twits.objects.get(text="test text twit_2")
    tags_db = twit_from_db.tag.all()
    profile = Profiles.objects.get(username="testuser3")
    twit, tags, twits_ansver, like_twit, repost_twit = get_tweet_for_viewing(
        twit_id=twit_from_db.pk, profile=profile
    )
    assert twit == twit_from_db
    assert list(tags_db) == tags
    assert type(twits_ansver) == list
    assert len(twits_ansver) == 1
    assert type(twits_ansver[0]) == Twits
    assert twits_ansver[0].text == "test text twit_5"
    assert like_twit is False
    assert repost_twit is True


@pytest.mark.django_db
def test_get_tweet_for_viewing_raise_getvalueerror() -> None:
    twit = Twits.objects.all().order_by("-id")[0]
    twit_id = twit.pk + 1
    profile = Profiles.objects.get(username="testuser3")
    with pytest.raises(GetValueError):
        get_tweet_for_viewing(twit_id=twit_id, profile=profile)


@pytest.mark.django_db
def test_view_twits_succssefully() -> None:
    twit_from_db = Twits.objects.get(text="test text twit_2")
    tags_db = twit_from_db.tag.all()
    twit, tag, twits_ansver = view_twits(twit_id=twit_from_db.pk)
    assert twit == twit_from_db
    assert list(tags_db) == tag
    assert type(twits_ansver) == list
    assert len(twits_ansver) == 1
    assert type(twits_ansver[0]) == Twits
    assert twits_ansver[0].text == "test text twit_5"


@pytest.mark.django_db
def test_view_twits_raise_getvalueerror() -> None:
    twit = Twits.objects.all().order_by("-id")[0]
    twit_id = twit.pk + 1
    with pytest.raises(GetValueError):
        view_twits(twit_id=twit_id)
