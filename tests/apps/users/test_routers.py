import uuid

import pytest
from fastapi import status

from .factories import UserFactory
from web_app.apps.users.models import User as UserModel


@pytest.fixture
def user_id():
    return str(uuid.uuid4())


@pytest.mark.asyncio
async def test_search(client, user_data):
    user = await UserFactory.create()

    response = client.get(f"/users/?q={user.username}")
    assert response.status_code == status.HTTP_200_OK

    data = response.json()
    assert len(data) == 1


@pytest.mark.asyncio
async def test_search_with_pagination_limit_offset(client, user_data):
    await UserFactory.create()
    await UserFactory.create(**user_data)

    user_name = user_data["username"]
    response = client.get(f"/users/?q={user_name}&limit=1&offset=0")
    assert response.status_code == status.HTTP_200_OK

    data = response.json()
    assert len(data) == 1
    assert len(await UserModel.query.gino.all()) == 2


def test_search_without_results(client):
    response = client.get("/users/?name=Some Name")

    assert response.status_code == status.HTTP_200_OK

    data = response.json()
    assert len(data) == 0
