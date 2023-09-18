from __future__ import annotations

from typing import TYPE_CHECKING

from core.models import Tags

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
