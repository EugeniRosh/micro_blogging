# mypy: ignore-errors
from datetime import datetime

import pytest
from core.presentation.validators import (
    ValdateMaxValue,
    ValidateFileExtension,
    ValidateFileSize,
    ValidationAge,
)
from core.tests.mocks import FileMock
from django.core.exceptions import ValidationError


@pytest.mark.django_db
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


@pytest.mark.django_db
class TestValdateMaxValue:
    validation = ValdateMaxValue(max_count=5)

    def test_validation_max_value_successfully(self) -> None:
        value = ["test" for _ in range(self.validation._max_count)]
        value_str = "\r\n".join(value)
        result = self.validation(value=value_str)
        assert result is None

        value_is_less = ["test" for _ in range(self.validation._max_count - 1)]
        value_is_less_str = "\r\n".join(value_is_less)
        result_less = self.validation(value=value_is_less_str)
        assert result_less is None

    def test_counter_overrun_validation(self) -> None:
        value = ["test" for _ in range(self.validation._max_count + 1)]
        value_str = "\r\n".join(value)
        with pytest.raises(ValidationError):
            self.validation(value=value_str)


@pytest.mark.django_db
class TestValidateFileExtension:
    validation = ValidateFileExtension(available_extensions=["pdf"])

    def test_validation_file_extension_successfully(self) -> None:
        file_mock = FileMock(name="test.pdf")
        result = self.validation(value=file_mock)
        assert result is None

    def test_validation_missing_file_extension(self) -> None:
        file_mock = FileMock(name="test")
        with pytest.raises(ValidationError):
            self.validation(value=file_mock)

    def test_validation_incorrect_file_extensions(self) -> None:
        file_mock = FileMock(name="test.jpg")
        with pytest.raises(ValidationError):
            self.validation(value=file_mock)


@pytest.mark.django_db
class TestValidateFileSize:
    validation = ValidateFileSize(max_size=5_000_000)

    def test_validation_file_size(self) -> None:
        file_mock = FileMock(size=4_050_000)
        result = self.validation(value=file_mock)
        assert result is None

    def test_validation_oversize(self) -> None:
        file_mock = FileMock(size=5_050_000)
        with pytest.raises(ValidationError):
            self.validation(value=file_mock)
