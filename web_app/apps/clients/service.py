import asyncio
from urllib.parse import urljoin

import aiohttp
from fastapi import HTTPException

from web_app.config import settings


def build_product_url(external_id):
    url = urljoin(settings.PRODUCTS_API, str(external_id))
    url = url + "/"  # particulary from api
    return url


async def load_products(clients):
    tasks = [load_product(c) for c in clients]
    clients_updates = await asyncio.gather(*tasks)
    return clients_updates


async def load_product(client):
    client.favorite_products = await get_products(client.products)
    return client


async def validate_product(external_id):
    async with aiohttp.ClientSession() as session:
        url = build_product_url(external_id)
        async with session.get(url) as response:
            if response.status != 200:
                raise HTTPException(
                    status_code=400,
                    detail=f"Product {external_id} not found.",
                )
            payload = await response.json()
            return payload


async def get_product(session, external_id):
    url = build_product_url(external_id)
    async with session.get(url) as response:
        if response.status == 200:
            product_requested = await response.json()
            return product_requested


async def get_products(products):
    async with aiohttp.ClientSession() as session:
        tasks = [get_product(session, products.external_id) for products in products]
        requested_products = await asyncio.gather(*tasks)
        requested_products = [product for product in requested_products if product is not None]
        return requested_products
