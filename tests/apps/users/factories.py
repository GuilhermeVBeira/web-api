from tests.factory import BaseFactory
from web_app.apps.users.models import User


class UserFactory(BaseFactory):
    class Meta:
        model = User

    username = "username"
    email = "user1@email.com"
    password = "supersecret"
    is_active = True
