from django.db import models

from .base_model import BaseModel


class Twits(BaseModel):
    text = models.CharField(max_length=400)
    answer_to_twit = models.ForeignKey(
        to="twits",
        related_name="answer",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    profile = models.ForeignKey(
        to="profiles", related_name="twits", on_delete=models.CASCADE
    )
    tag = models.ManyToManyField(
        to="tags",
        through="twitstags",
    )
    like = models.ManyToManyField(
        to="profiles", through="twitsprofileslikes", related_name="likes"
    )
    repost = models.ManyToManyField(
        to="profiles", through="twitsprofilesreposts", related_name="reposts"
    )

    class Meta:
        db_table = "twits"
