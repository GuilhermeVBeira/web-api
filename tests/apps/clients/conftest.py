import pytest

from web_app.config import settings


@pytest.fixture
def product_data():
    return {
        "price": 1699.0,
        "image": f"{settings.PRODUCTS_API}1bf0f365-fbdd-4e21-9786-da459d78dd1f.jpg",
        "brand": "bébé confort",
        "id": "1bf0f365-fbdd-4e21-9786-da459d78dd1f",
        "title": "Cadeira para Auto Iseos Bébé Confort Earth Brown"
    }


@pytest.fixture
def client_data():
    return {"id": "a72fcbe5-1103-4acc-a77b-954b46bc7ba8", "email": "naruto@uzumaki.com", "username": "naruto"}
