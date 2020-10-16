import uuid
from unittest import mock

import pytest
from fastapi import status

from .factories import ClientFactory, FavoriteProductFactory
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
    assert response.json() == {"detail": "The user with this email already exists in the system."}


@pytest.mark.asyncio
@mock.patch("web_app.apps.clients.service.get_product", new_callable=mock.AsyncMock)
async def test_search_with_pagination_limit_offset(mock_get_product, product_data, client, client_data):
    mock_get_product.return_value = product_data

    first_client = await ClientFactory.create()
    second_client = await ClientFactory.create(email="second@email.com")
    await FavoriteProductFactory.create(client_id=first_client.id)
    await FavoriteProductFactory.create(client_id=second_client.id)

    user_name = first_client.username
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
@mock.patch("web_app.apps.clients.service.get_product", new_callable=mock.AsyncMock)
async def test_get(mock_get_product, product_data, client, client_data):
    mock_get_product.return_value = product_data

    client_created = await ClientFactory.create()
    await FavoriteProductFactory.create(client_id=client_created.id)

    response = client.get(f"/clients/{client_created.id}")

    assert response.status_code == status.HTTP_200_OK

    data = response.json()

    assert data["id"]
    assert data["username"] == client_data["username"]
    assert data["email"] == client_data["email"]

    assert len(data["favorite_products"]) == 1

    response_product = data["favorite_products"][0]
    assert response_product["id"] == product_data["id"]
    assert mock_get_product.called is True


@pytest.mark.asyncio
async def test_delete(client, client_data):
    client_model = await ClientFactory.create()

    response = client.delete(f"/clients/{client_model.id}")

    assert response.status_code == status.HTTP_204_NO_CONTENT


def test_delete_not_found(client):
    client_id = str(uuid.uuid4())
    response = client.delete(f"/clients/{client_id}")

    assert response.status_code == status.HTTP_404_NOT_FOUND
