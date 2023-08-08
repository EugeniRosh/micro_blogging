from django.db import models

from .base_model import BaseModel


class TwitsProfilesLikes(BaseModel):
    profile = models.ForeignKey(
        to="profiles", related_name="twits_like", on_delete=models.CASCADE
    )
    twit = models.ForeignKey(
        to="twits", related_name="profiles_like", on_delete=models.CASCADE
    )

    class Meta:
        db_table = "twits_profiles_likes"
        constraints = [
            models.UniqueConstraint(fields=["twit", "profile"], name="unique_likes")
        ]
