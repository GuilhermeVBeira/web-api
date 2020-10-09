import pytest
from pydantic import ValidationError

from web_app.apps.users.schemas import User, UserCreate


def test_create_user_missing_required_atribute(user_data):
    user_data.pop("email")

    with pytest.raises(ValidationError):
        User(**user_data)


def test_create_user_with_invalid_email(user_data):
    user_data["email"] = "email"

    with pytest.raises(ValidationError) as exc:
        UserCreate(**user_data)

    assert "value is not a valid email address" in str(exc)


def test_create_user_with_invalid_password_length(user_data):
    user_data["password"] = "1"

    with pytest.raises(ValidationError) as exc:
        UserCreate(**user_data)

    assert "ensure this value has at least 6 characters" in str(exc)


def test_user_string_conversion(user_data):
    user = User(**user_data)

    expected_str = f"{user.id}, {user.username}, {user.email}"

    assert str(user) == expected_str


def test_create_user(user_data):
    user = User(**user_data)

    assert str(user.id) == user_data["id"]
    assert user.email == user_data["email"]
    assert user.is_active == user_data["is_active"]
    assert user.username == user_data["username"]
    assert user.Config.orm_mode is True


def test_user_hash_password(user_data):
    user = UserCreate(**user_data)

    assert user.hash_password()


def test_user_hash_password_already_hashed(user_data):
    user = UserCreate(**user_data)

    user.password = user.hash_password()

    assert user.hash_password() is None


def test_user_hash_password_without_password_filled(user_data):
    user_data.pop("password")

    user = UserCreate(**user_data)

    assert user.hash_password() is None
