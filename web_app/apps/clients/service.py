import asyncio
from urllib.parse import urljoin

import aiohttp

from web_app.config import settings


async def get_product(external_id):
    async with aiohttp.ClientSession() as session:
        url = urljoin(settings.PRODUCTS_API, str(external_id))
        url = url + "/"  # particulary from api
        async with session.get(url) as response:
            if response.status == 200:
                product_requested = await response.json()
                return product_requested


async def get_products(products):
    tasks = [get_product(products.external_id) for products in products]
    requested_products = await asyncio.gather(*tasks)
    requested_products = [product for product in requested_products if product is not None]
    return requested_products
