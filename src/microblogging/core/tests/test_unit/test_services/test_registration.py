from datetime import datetime
from time import time

import pytest
from core.business_logic.dto import RegistrationDTO
from core.business_logic.exceptions import (
    CreateUniqueError,
    ExpirationTimeError,
    GetValueError,
)
from core.business_logic.services import regisration_user, registration_confirmations
from core.models import EmailConfirmationCode, Profiles


@pytest.mark.django_db
def test_regisration_user_successfully() -> None:
    data_test = RegistrationDTO(
        username="testuser999",
        email="testemail@gmail.com",
        password="123456",
        date_of_birth=datetime(year=2000, month=3, day=5),
    )
    result = regisration_user(data=data_test)
    assert type(result) == int

    profile = Profiles.objects.get(pk=result)
    assert profile.username == "testuser999"
    assert profile.email == "testemail@gmail.com"
    assert profile.date_of_birth.year == 2000
    assert profile.date_of_birth.month == 3
    assert profile.date_of_birth.day == 5


@pytest.mark.django_db
def test_regisration_user_raise_createuniqueerror_username() -> None:
    data_test = RegistrationDTO(
        username="testuser3",
        email="testemail@gmail.com",
        password="123456",
        date_of_birth=datetime(year=2000, month=3, day=5),
    )
    with pytest.raises(CreateUniqueError):
        regisration_user(data=data_test)


@pytest.mark.django_db
def test_regisration_user_raise_createuniqueerror_email() -> None:
    data_test = RegistrationDTO(
        username="testuser999",
        email="testuser3@gmail.com",
        password="123456",
        date_of_birth=datetime(year=2000, month=3, day=5),
    )
    with pytest.raises(CreateUniqueError):
        regisration_user(data=data_test)


@pytest.mark.django_db
def test_registration_confirmations_successfully() -> None:
    test_code = "testconfirmationscode"
    profile = Profiles.objects.get(username="testuser3")
    EmailConfirmationCode.objects.create(
        code=test_code,
        profile=profile,
        expiration=10 + int(time()),
    )
    result = registration_confirmations(confirmation_code=test_code)  # type: ignore

    assert result is None
    with pytest.raises(EmailConfirmationCode.DoesNotExist):
        EmailConfirmationCode.objects.get(code=test_code)

    profile.refresh_from_db()
    assert profile.is_active is True


@pytest.mark.django_db
def test_registration_confirmations_raise_getvalueerror() -> None:
    test_code = "testconfirmationscode"
    with pytest.raises(GetValueError):
        registration_confirmations(confirmation_code=test_code)


@pytest.mark.django_db
def test_registration_confirmations_raise_expirationtimeerror() -> None:
    test_code = "testconfirmationscode"
    profile = Profiles.objects.get(username="testuser3")
    EmailConfirmationCode.objects.create(
        code=test_code,
        profile=profile,
        expiration=int(time()) - 10,
    )
    with pytest.raises(ExpirationTimeError):
        registration_confirmations(confirmation_code=test_code)
