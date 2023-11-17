import pytest
from core.business_logic.services.twits import (
    get_twits_and_counts_of_likes_of_reposts_of_answer,
)
from core.models import Twits
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
