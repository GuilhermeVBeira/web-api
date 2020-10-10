import pytest
from pydantic import ValidationError

from web_app.apps.clients.schemas import Client


def test_create_client_missing_required_atribute(client_data):
    client_data.pop("email")

    with pytest.raises(ValidationError):
        Client(**client_data)


def test_create_client_with_invalid_email(client_data):
    client_data["email"] = "email"

    with pytest.raises(ValidationError) as exc:
        Client(**client_data)

    assert "value is not a valid email address" in str(exc)
