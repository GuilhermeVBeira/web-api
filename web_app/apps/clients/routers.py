import asyncio
import typing
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status

from web_app.apps.auth.authentication import validate_token
from web_app.apps.clients.models import Client as ClientModel
from web_app.apps.clients.models import FavoriteProduct
from web_app.apps.clients.schemas import ClientProductsRequest, ClientProductsResponse
from web_app.apps.clients.service import load_product, load_products, validate_product
from web_app.main import db
from web_app.pagination import Pagination

router = APIRouter()


@router.post(
    "/clients/",
    dependencies=[Depends(validate_token)],
    status_code=status.HTTP_201_CREATED,
    response_model=ClientProductsResponse,
)
async def client_create(client: ClientProductsRequest):
    query = ClientModel.query.where(ClientModel.email == client.email)
    email_exists = await query.gino.first()
    if email_exists:
        raise HTTPException(
            status_code=400,
            detail="The client with this email already exists in the system.",
        )
    # validate from external service
    to_validate = [validate_product(product.id) for product in client.favorite_products]
    valid_products = await asyncio.gather(*to_validate)
    async with db.transaction():
        client_created = await ClientModel.create(
            username=client.username,
            email=client.email,
        )
        favorite_products = [
            dict(external_id=p.id, client_id=client_created.id) for p in client.favorite_products
        ]
        await FavoriteProduct.insert().gino.all(favorite_products)
    client_created.favorite_products = valid_products
    return client_created


@router.get(
    "/clients/{client_id}",
    description="Endpoint to fetch client",
    dependencies=[Depends(validate_token)],
    response_model=ClientProductsResponse,
)
async def client_get(client_id: UUID):
    query = FavoriteProduct.outerjoin(ClientModel).select()
    loader = ClientModel.distinct(ClientModel.id).load(add_product=FavoriteProduct)
    client = await query.where(ClientModel.id == client_id).gino.load(loader).all()
    if not client:
        raise HTTPException(
            status_code=404,
            detail="Not found client",
        )
    client = await load_product(client[0])
    return client


@router.get(
    "/clients/",
    description="Endpoint to search clients",
    response_model=typing.List[ClientProductsResponse],
    dependencies=[Depends(validate_token)],
)
async def clients_search(p: Pagination = Depends()):
    query = FavoriteProduct.outerjoin(ClientModel).select()
    loader = ClientModel.distinct(ClientModel.id).load(add_product=FavoriteProduct)
    if p.q is None:
        query = query.limit(p.limit).offset(p.offset)
    else:
        query = query.where(ClientModel.username == p.q).limit(p.limit).offset(p.offset)
    clients = await query.gino.load(loader).all()
    return await load_products(clients)


@router.delete(
    "/clients/{client_id}", status_code=status.HTTP_204_NO_CONTENT, dependencies=[Depends(validate_token)]
)
async def clients_delete(client_id: UUID):
    client = await ClientModel.get_or_404(client_id)
    await client.delete()


@router.put(
    "/clients/{client_id}",
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(validate_token)],
    response_model=ClientProductsResponse,
)
async def clients_update(client_id: UUID, client: ClientProductsRequest):
    async with db.transaction():
        client_ = await ClientModel.get_or_404(client_id)
        to_validate = [validate_product(product.id) for product in client.favorite_products]
        valid_products = await asyncio.gather(*to_validate)

        await client_.update(username=client.username, email=client.email).apply()
        await FavoriteProduct.delete.where(FavoriteProduct.client_id == client_.id).gino.status()
        favorite_products = [dict(external_id=p.id, client_id=client_.id) for p in client.favorite_products]
        await FavoriteProduct.insert().gino.all(favorite_products)
        client.id = client_.id
        client.favorite_products = valid_products
        return client


def include_router(app):
    app.include_router(router)
