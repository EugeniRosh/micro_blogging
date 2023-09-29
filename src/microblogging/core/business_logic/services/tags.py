from __future__ import annotations

from datetime import datetime, timedelta
from typing import TYPE_CHECKING

from core.models import Tags
from django.db.models import Count

if TYPE_CHECKING:
    from django.db.models.query import QuerySet


def get_tags(tags: str) -> list[Tags]:
    tags_list: list[Tags] = []
    tags_split = tags.split("\r\n")

    for tag in tags_split:
        tag_db, tag_bool = Tags.objects.get_or_create(tag=tag.lower())

        tags_list.append(tag_db)

    return tags_list


def get_a_tag_to_search_for_tweets(tag: str) -> QuerySet:
    search_tag = Tags.objects.filter(tag=tag)
    return search_tag


def trending_in_your_country(country: str) -> QuerySet:
    date = datetime.today()
    date_to_search = date - timedelta(days=1)

    tags = (
        Tags.objects.filter(
            twit_tag__twit__profile__country=country,
            twit_tag__twit__created_at__date=date_to_search.date(),
        )
        .annotate(count_tag=Count("tag"))
        .order_by("-count_tag")[:10]
    )

    return tags
