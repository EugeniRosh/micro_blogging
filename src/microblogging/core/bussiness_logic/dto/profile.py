from dataclasses import dataclass
from datetime import datetime

from django.core.files.uploadedfile import InMemoryUploadedFile


@dataclass
class ProfileDTO:
    username: str | None
    first_name: str | None
    last_name: str | None
    password: str | None
    email: str | None
    country: str | None
    photo: InMemoryUploadedFile | None
    description: str | None
    date_of_birth: str | None
    date_joined: datetime | None
