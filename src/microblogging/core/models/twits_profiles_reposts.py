from django.db import models

from .base_model import BaseModel


class TwitsProfilesReposts(BaseModel):
    profile = models.ForeignKey(
        to="profiles", related_name="twits_repost", on_delete=models.CASCADE
    )
    twit = models.ForeignKey(
        to="twits", related_name="profiles_repost", on_delete=models.CASCADE
    )

    class Meta:
        db_table = "twits_profiles_reposts"
        constraints = [
            models.UniqueConstraint(fields=["twit", "profile"], name="unique_reposts")
        ]
