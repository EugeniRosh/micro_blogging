from django.db import models

from .base_model import BaseModel


class TwitsTags(BaseModel):
    twit = models.ForeignKey(
        to="twits", related_name="tags_twit", on_delete=models.CASCADE
    )
    tag = models.ForeignKey(
        to="tags", related_name="twit_tag", on_delete=models.CASCADE
    )

    class Meta:
        db_table = "twits_tags"
        constraints = [
            models.UniqueConstraint(fields=["twit", "tag"], name="unique_twits_tags")
        ]
