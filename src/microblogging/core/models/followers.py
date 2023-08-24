from django.db import models

from .base_model import BaseModel


class Followers(BaseModel):
    follower = models.ForeignKey(
        to="profiles", related_name="user_follower", on_delete=models.CASCADE
    )
    following = models.ForeignKey(
        to="profiles", related_name="user_following", on_delete=models.CASCADE
    )

    class Meta:
        db_table = "followers"
        constraints = [
            models.UniqueConstraint(
                fields=["follower", "following"], name="unique_followers"
            )
        ]
