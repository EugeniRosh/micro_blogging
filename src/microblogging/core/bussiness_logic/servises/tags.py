from core.models import Tags


def get_tegs(tags: str) -> list[Tags]:
    tags_list: list[Tags] = []
    tags_split = tags.split("\r\n")

    for tag in tags_split:
        tag_db, tag_bool = Tags.objects.get_or_create(tag=tag.lower())

        tags_list.append(tag_db)

    return tags_list
