import asyncio
from collections import namedtuple
from uuid import uuid4

import pytest
from aioresponses import aioresponses

from web_app.apps.clients.service import get_product, get_products
from web_app.config import settings


@pytest.mark.asyncio
async def test_get_product(product_data):
    url = f"{settings.PRODUCTS_API}1bf0f365-fbdd-4e21-9786-da459d78dd1f/"
    with aioresponses() as mocked:
        mocked.get(url, status=200,  payload=product_data)
        product = asyncio.run(get_product("1bf0f365-fbdd-4e21-9786-da459d78dd1f"))

        assert product == product_data


@pytest.mark.asyncio
async def test_get_product_not_found(product_data):
    url = f"{settings.PRODUCTS_API}1bf0f365-fbdd-4e21-9786-da459d78dd1f/"
    with aioresponses() as mocked:
        mocked.get(url, status=404)
        product = asyncio.run(get_product("1bf0f365-fbdd-4e21-9786-da459d78dd1f"))

        assert product is None


@pytest.mark.asyncio
async def test_get_products(product_data):
    Product = namedtuple("Product", "external_id")
    first_product = Product(external_id=uuid4())
    second_product = Product(external_id=uuid4())
    with aioresponses() as mocked:
        url = f"{settings.PRODUCTS_API}{first_product.external_id}/"
        mocked.get(url, status=404)
        url = f"{settings.PRODUCTS_API}{second_product.external_id}/"
        mocked.get(url, status=200,  payload=product_data)
        products = await get_products([first_product, second_product])
    assert products == [product_data]
