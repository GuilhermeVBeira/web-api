from unittest import mock

import pytest
from click.testing import CliRunner

from web_app.apps.users.models import User
from web_app.utils import create_user, createuser


@pytest.mark.asyncio
@mock.patch("web_app.utils.db.set_bind", new_callable=mock.AsyncMock)
async def test_create_user(mock_set_bind, client):
    all_existends_users = await User.query.gino.all()
    assert len(all_existends_users) == 0
    await create_user("username", "email@email.com", "password")
    all_users = await User.query.gino.all()
    assert len(all_users) == 1
    assert mock_set_bind.called is True


@pytest.mark.asyncio
@mock.patch("web_app.utils.create_user", new_callable=mock.AsyncMock)
async def test_hello_world(mock_create_user):
    runner = CliRunner()
    user_input = "admin\nemail@emal\npassword\npassword"
    result = runner.invoke(createuser, input=user_input)
    assert "User admin created" in result.output
    assert mock_create_user.called is True
