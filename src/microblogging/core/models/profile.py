from django.contrib.auth import get_user_model
from django.db import models

from .base_model import BaseModel


class Profiles(BaseModel):
    name = models.CharField(max_length=100, blank=True)
    surname = models.CharField(max_length=100, blank=True)
    country = models.CharField(max_length=100, blank=True)
    photo = models.CharField(max_length=100, blank=True)
    date_of_birth = models.DateTimeField(null=True)
    auth_user = models.OneToOneField(
        to=get_user_model(), related_name="profiles", on_delete=models.CASCADE
    )
    followers = models.ManyToManyField(to="profiles", through="followers")
    notification = models.ManyToManyField(
        to="twits", through="twitsprofilesnotifications"
    )

    class Meta:
        db_table = "profiles"
