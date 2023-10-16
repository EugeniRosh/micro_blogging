from __future__ import annotations

import os
from datetime import datetime

from django.core.exceptions import ValidationError
from django.core.files import File


class ValidationAge:
    def __init__(self, min_age: int) -> None:
        self._min_age = min_age

    def __call__(self, value: datetime) -> None:
        date = datetime.now()
        if date.year - value.year < self._min_age:
            raise ValidationError(
                message=f"Registration only for users over {self._min_age} years of age"
            )
        if date.year - value.year == self._min_age:
            if date.month - value.month < 0:
                raise ValidationError(
                    message=f"Registration only for users over {self._min_age} years of age"
                )
            if date.day - value.day < 0:
                raise ValidationError(
                    message=f"Registration only for users over {self._min_age} years of age"
                )


class ValidateFileExtension:
    def __init__(self, available_extensions: list[str]) -> None:
        self._available_extensions = available_extensions

    def __call__(self, value: File) -> None:
        _, file_extension = os.path.splitext(value.name)

        if not file_extension:
            raise ValidationError(message="File must have an extension")

        if file_extension[1:] not in self._available_extensions:
            raise ValidationError(message=f"Accept only {self._available_extensions}")


class ValidateFileSize:
    def __init__(self, max_size: int) -> None:
        self._max_size = max_size

    def __call__(self, value: File) -> None:
        if value.size > self._max_size:
            max_size_in_mb = int(self._max_size / 1_000_000)
            raise ValidationError(message=f"Max file size is {max_size_in_mb} MB")


class ValdateMaxValue:
    def __init__(self, max_count: int) -> None:
        self._max_count = max_count

    def __call__(self, value: str) -> None:
        value_split = value.split('\r\n')
        if len(value_split) > self._max_count:
            raise ValidationError(message=f"Max value must be {self._max_count}")
