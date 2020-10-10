from fastapi import status
import pytest
from .factories import ClientFactory


def test_create(client, client_data):
    response = client.post("/clients/", json=client_data)

    assert response.status_code == status.HTTP_201_CREATED

    user = response.json()

    assert user["id"]
    assert user["username"] == client_data["username"]
    assert user["email"] == client_data["email"]


def test_create_exist_email(client, client_data):
    client.post("/clients/", json=client_data)
    response = client.post("/clients/", json=client_data)

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json() == {'detail': 'The user with this username already exists in the system.'}
