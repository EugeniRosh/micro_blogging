from django.contrib.auth.models import AbstractUser
from django.db import models


class Profiles(AbstractUser):
    email = models.CharField(max_length=100, unique=True)
    country = models.CharField(max_length=100, blank=True)
    photo = models.CharField(max_length=100, blank=True)
    date_of_birth = models.DateTimeField(null=True)
    followers = models.ManyToManyField(to="profiles", through="followers")
    notification = models.ManyToManyField(
        to="twits", through="twitsprofilesnotifications"
    )
    update_at = models.DateField(auto_now=True)

    USERNAME_FIELD = "email"

    REQUIRED_FIELDS = ["username", "date_of_birth"]

    class Meta:
        db_table = "profiles"
