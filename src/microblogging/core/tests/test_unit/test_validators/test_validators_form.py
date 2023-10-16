# mypy: ignore-errors
from datetime import datetime

import pytest
from core.presentation.validators import ValidationAge
from django.core.exceptions import ValidationError


def test_validation_age_successfully() -> None:
    validation = ValidationAge(min_age=18)
    age_for_validation = datetime(2000, 1, 1)
    result = validation(value=age_for_validation)
    assert result is None


def test_validation_of_minimum_age_years() -> None:
    validation = ValidationAge(min_age=18)
    age_for_validation = datetime.now()
    with pytest.raises(ValidationError):
        validation(value=age_for_validation)


def test_validation_of_minimum_age_month() -> None:
    validation = ValidationAge(min_age=18)
    date = datetime.now()
    age_for_validation = datetime(
        year=date.year - 18, month=date.month + 1, day=date.day
    )
    with pytest.raises(ValidationError):
        validation(value=age_for_validation)


def test_validation_of_minimum_age_day() -> None:
    validation = ValidationAge(min_age=18)
    date = datetime.now()
    age_for_validation = datetime(
        year=date.year - 18, month=date.month, day=date.day + 1
    )
    with pytest.raises(ValidationError):
        validation(value=age_for_validation)
