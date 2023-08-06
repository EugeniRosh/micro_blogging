from django.db import models

from .base_model import BaseModel


class Tags(BaseModel):
    tag = models.CharField(max_length=20, unique=True)

    class Meta:
        db_table = "tags"
