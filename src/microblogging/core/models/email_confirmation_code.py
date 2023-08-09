from django.contrib.auth import get_user_model
from django.db import models

from .base_model import BaseModel


class EmailConfirmationCode(BaseModel):
    code = models.CharField(max_length=100)
    profile = models.ForeignKey(
        to=get_user_model(),
        related_name="emailconfirmationcode",
        on_delete=models.CASCADE,
    )
    expiration = models.PositiveIntegerField()

    class Meta:
        db_table = "email_confirmation_codes"
