import nest_asyncio
import pytest
from alembic.config import main
from fastapi.testclient import TestClient
from jose import jwt

from web_app.config import settings
from web_app.main import db, get_app

settings.TEST_ENV = True

# because the http test client runs an event loop fot itself,
# this lib is necessary to avoid the errror "this event loop
# is already running"
nest_asyncio.apply()


@pytest.fixture
def client():
    main(["--raiseerr", "upgrade", "head"])
    test_app = get_app(db, settings.TEST_DATABASE_URL)
    encoded_jwt = jwt.encode({"sub": "username"}, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    with TestClient(test_app) as client:
        token = f"bearer {encoded_jwt}"
        client.headers.update({"Authorization": token})
        yield client

    main(["--raiseerr", "downgrade", "base"])
