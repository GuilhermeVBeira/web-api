from fastapi import status
import pytest
from web_app.apps.clients.models import Client as ClientModel
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

