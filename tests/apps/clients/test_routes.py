import uuid

import pytest
from fastapi import status

from .factories import ClientFactory
from web_app.apps.clients.models import Client as ClientModel


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
    assert response.json() == {"detail": "The user with this username already exists in the system."}


@pytest.mark.asyncio
async def test_search_with_pagination_limit_offset(client, client_data):
    await ClientFactory.create(email="random@email.com")
    await ClientFactory.create(**client_data)

    user_name = client_data["username"]
    response = client.get(f"/clients/?q={user_name}&limit=1&offset=0")
    assert response.status_code == status.HTTP_200_OK

    data = response.json()
    assert len(data) == 1
    assert len(await ClientModel.query.gino.all()) == 2


def test_search_without_results(client):
    response = client.get("/clients/?name=Some Name")

    assert response.status_code == status.HTTP_200_OK

    data = response.json()
    assert len(data) == 0


def test_get_not_found(client):
    client_id = str(uuid.uuid4())
    response = client.get(f"/clients/{client_id}")

    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.asyncio
async def test_get(client, client_data):
    client_model = await ClientFactory.create()

    response = client.get(f"/clients/{client_model.id}")

    assert response.status_code == status.HTTP_200_OK

    data = response.json()

    assert data["id"]
    assert data["username"] == client_data["username"]
    assert data["email"] == client_data["email"]
