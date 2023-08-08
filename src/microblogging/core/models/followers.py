from django.db import models

from .base_model import BaseModel


class Followers(BaseModel):
    profile = models.ForeignKey(
        to="profiles", related_name="follower_profile", on_delete=models.CASCADE
    )
    follower_profile = models.ForeignKey(
        to="profiles", related_name="follower", on_delete=models.CASCADE
    )

    class Meta:
        db_table = "followers"
        constraints = [
            models.UniqueConstraint(
                fields=["profile", "follower_profile"], name="unique_followers"
            )
        ]
