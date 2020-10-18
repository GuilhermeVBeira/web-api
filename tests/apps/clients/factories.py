from uuid import uuid4

from tests.factory import BaseFactory
from web_app.apps.clients.models import Client, FavoriteProduct


class FavoriteProductFactory(BaseFactory):
    class Meta:
        model = FavoriteProduct

    external_id = uuid4().hex
    client_id = uuid4().hex


class ClientFactory(BaseFactory):
    class Meta:
        model = Client

    username = "naruto"
    email = "naruto@uzumaki.com"
