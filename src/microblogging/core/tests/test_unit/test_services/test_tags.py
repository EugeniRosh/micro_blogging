import pytest
from core.business_logic.services.tags import get_a_tag_to_search_for_tweets, get_tags
from core.models import Tags
from django.db.models.query import QuerySet
from django.db.utils import DataError


@pytest.mark.django_db
def test_get_tags_successfully() -> None:
    tags = "test\r\npytest\r\npython"
    list_tags = get_tags(tags=tags)
    assert type(list_tags) == list
    assert len(list_tags) == 3
    assert type(list_tags[0]) == Tags


@pytest.mark.django_db
def test_get_tags_exceeding_max_len() -> None:
    tags = "t" * 21
    with pytest.raises(DataError):
        get_tags(tags=tags)


@pytest.mark.django_db
def test_get_a_tag_to_search_for_tweets_successfuly() -> None:
    tag = "sql"
    search_tag = get_a_tag_to_search_for_tweets(tag=tag)
    assert type(search_tag) == QuerySet
    assert len(search_tag) == 1
    assert type(search_tag[0]) == Tags
    assert search_tag[0].tag == tag


@pytest.mark.django_db
def test_get_a_tag_to_search_for_tweets_non_existent_tag() -> None:
    tag = "test"
    search_tag = get_a_tag_to_search_for_tweets(tag=tag)
    assert type(search_tag) == QuerySet
    assert len(search_tag) == 0
