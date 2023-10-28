import pytest
from core.business_logic.services.send_an_mail import send_confirmation_code
from core.models import EmailConfirmationCode, Profiles


@pytest.mark.django_db
def test_send_confirmation_code_successfully() -> None:
    profile = Profiles.objects.get(username="testuser2")
    send_confirmation_code(user=profile, email=profile.email)
    email_code = EmailConfirmationCode.objects.get(profile=profile)
    assert email_code is not None
