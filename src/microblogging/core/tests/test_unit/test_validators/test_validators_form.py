# mypy: ignore-errors
from datetime import datetime

import pytest
from core.presentation.validators import ValidationAge
from django.core.exceptions import ValidationError


class TestValidationAge:
    validation = ValidationAge(min_age=18)

    def test_validation_age_successfully(self) -> None:
        age_for_validation = datetime(2000, 1, 1)
        result = self.validation(value=age_for_validation)
        assert result is None

    def test_validation_of_minimum_age_years(self) -> None:
        age_for_validation = datetime.now()
        with pytest.raises(ValidationError):
            self.validation(value=age_for_validation)

    def test_validation_of_minimum_age_month(self) -> None:
        date = datetime.now()
        age_for_validation = datetime(
            year=date.year - 18, month=date.month + 1, day=date.day
        )
        with pytest.raises(ValidationError):
            self.validation(value=age_for_validation)

    def test_validation_of_minimum_age_day(self) -> None:
        date = datetime.now()
        age_for_validation = datetime(
            year=date.year - 18, month=date.month, day=date.day + 1
        )
        with pytest.raises(ValidationError):
            self.validation(value=age_for_validation)
