from tests.factory import BaseFactory
from web_app.apps.clients.models import Client


class ClientFactory(BaseFactory):
    class Meta:
        model = Client

    username = "naruto"
    email = "naruto@uzumaki.com"
