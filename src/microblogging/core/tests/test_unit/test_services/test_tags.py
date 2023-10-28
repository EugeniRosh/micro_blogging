import pytest
from core.business_logic.services.tags import get_tags
from core.models import Tags
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
