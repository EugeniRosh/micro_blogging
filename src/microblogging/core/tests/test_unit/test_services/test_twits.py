import pytest
from core.business_logic.dto import TwitsDTO
from core.business_logic.exceptions import GetValueError, ProfileAccessError
from core.business_logic.services.twits import (
    add_a_twits,
    creat_answer_to_twit,
    delete_twits,
    get_info_twit_for_edit,
    get_profile_like_on_twit,
    get_profile_repost_on_twit,
    get_repost_twit,
    get_tweet_for_viewing,
    get_twit_by_id,
    get_twits,
    get_twits_and_counts_of_likes_of_reposts_of_answer,
    get_twits_and_reposts,
    view_twits,
)
from core.models import Profiles, Tags, Twits
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


@pytest.mark.django_db
def test_delete_twits_succssefully() -> None:
    profile = Profiles.objects.get(username="testuser1")
    twit = Twits.objects.get(text="test text twit_1")
    delete_twits(twit_id=twit.pk, profile=profile)
    twits = Twits.objects.filter(profile=profile)
    assert len(twits) == 2
    with pytest.raises(Twits.DoesNotExist):
        Twits.objects.get(text="test text twit_1")


@pytest.mark.django_db
def test_delete_twits_raise_profileaccesserror() -> None:
    profile = Profiles.objects.get(username="testuser2")
    twit = Twits.objects.get(text="test text twit_1")
    with pytest.raises(ProfileAccessError):
        delete_twits(twit_id=twit.pk, profile=profile)


@pytest.mark.django_db
def test_get_profile_like_on_twit_succssefully() -> None:
    profile_3 = Profiles.objects.get(username="testuser3")
    profile_2 = Profiles.objects.get(username="testuser2")
    twit = Twits.objects.get(text="test text twit_2")
    like_profile_3 = get_profile_like_on_twit(profile=profile_3, twit=twit)
    like_profile_2 = get_profile_like_on_twit(profile=profile_2, twit=twit)
    assert like_profile_3 is False
    assert like_profile_2 is True


@pytest.mark.django_db
def test_get_profile_repost_on_twit_succssefully() -> None:
    profile_3 = Profiles.objects.get(username="testuser3")
    profile_1 = Profiles.objects.get(username="testuser1")
    twit = Twits.objects.get(text="test text twit_6")
    like_profile_3 = get_profile_repost_on_twit(profile=profile_3, twit=twit)
    like_profile_1 = get_profile_repost_on_twit(profile=profile_1, twit=twit)
    assert like_profile_3 is False
    assert like_profile_1 is True


@pytest.mark.django_db
def test_creat_answer_to_twit_succssefully() -> None:
    twit = Twits.objects.get(text="test text twit_3")
    profile = Profiles.objects.get(username="testuser3")
    data = TwitsDTO(text="answer to twit", tag="python\r\nanswer\r\ntest")
    creat_answer_to_twit(twit_id=twit.pk, data=data, profile=profile)

    twit_list_for_test = Twits.objects.filter(answer_to_twit=twit)
    assert len(twit_list_for_test) == 1
    twit_for_test = twit_list_for_test[0]
    assert twit_for_test.text == "answer to twit"
    assert twit_for_test.profile == profile
    assert twit_for_test.answer_to_twit == twit
    tags = twit_for_test.tag.all()
    assert len(tags) == 3
    for tag in tags:
        assert tag.tag in ["python", "answer", "test"]


@pytest.mark.django_db
def test_creat_answer_to_twit_raise_getvalueerror() -> None:
    twit = Twits.objects.all().order_by("-id")[0]
    twit_id = twit.pk + 1
    profile = Profiles.objects.get(username="testuser3")
    data = TwitsDTO(text="answer to twit", tag="python\r\nanswer\r\ntest")
    with pytest.raises(GetValueError):
        creat_answer_to_twit(twit_id=twit_id, data=data, profile=profile)


@pytest.mark.django_db
def test_get_info_twit_for_edit_succssefully() -> None:
    twit = Twits.objects.get(text="test text twit_1")
    twit_for_test, tags_for_test = get_info_twit_for_edit(twit_id=twit.pk)
    assert twit_for_test == twit
    assert type(tags_for_test) == list
    assert len(tags_for_test) == 3
    assert type(tags_for_test[0]) == Tags
    for tag in tags_for_test:
        assert tag.tag in ["python", "sql", "postresql"]


@pytest.mark.django_db
def test_get_info_twit_for_edit_raise_getvalueerror() -> None:
    twit = Twits.objects.all().order_by("-id")[0]
    twit_id = twit.pk + 1
    with pytest.raises(GetValueError):
        get_info_twit_for_edit(twit_id=twit_id)
