from django.db import models

from .base_model import BaseModel


class TwitsProfilesNotifications(BaseModel):
    profile = models.ForeignKey(
        to="profiles", related_name="twits_notification", on_delete=models.CASCADE
    )
    twit = models.ForeignKey(
        to="twits", related_name="profiles_notification", on_delete=models.CASCADE
    )

    class Meta:
        db_table = "twits_profiles_notifications"
        constraints = [
            models.UniqueConstraint(
                fields=["twit", "profile"], name="unique_notification"
            )
        ]
