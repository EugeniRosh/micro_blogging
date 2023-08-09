from __future__ import annotations

from datetime import datetime

from django.core.exceptions import ValidationError


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

        return None
