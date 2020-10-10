import typing
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status

from web_app.apps.auth.authentication import validate_token
from web_app.apps.clients.models import Client as ClientModel
from web_app.apps.clients.schemas import Client
from web_app.pagination import Pagination

router = APIRouter()


@router.post(
    "/clients/",
    dependencies=[Depends(validate_token)],
    status_code=status.HTTP_201_CREATED,
    response_model=Client,
)
async def client_create(client: Client):
    query = ClientModel.query.where(ClientModel.email == client.email)
    email_exists = await query.gino.first()
    if email_exists:
        raise HTTPException(
            status_code=400,
            detail="The user with this username already exists in the system.",
        )
    user = await ClientModel.create(
        username=client.username,
        email=client.email,
    )
    return user


@router.get(
    "/clients/{client_id}",
    description="Endpoint to fetch client",
    response_model=Client,
    dependencies=[Depends(validate_token)],
)
async def client_get(client_id: UUID):
    client = await ClientModel.get_or_404(client_id)
    return client


@router.get(
    "/clients/",
    description="Endpoint to search clients",
    response_model=typing.List[Client],
    dependencies=[Depends(validate_token)],
)
async def users_search(p: Pagination = Depends()):
    if p.q is None:
        query = ClientModel.query.limit(p.limit).offset(p.offset)
    else:
        query = ClientModel.query.where(ClientModel.username == p.q).limit(p.limit).offset(p.offset)
    users = await query.gino.all()
    return users


@router.delete(
    "/clients/{client_id}", status_code=status.HTTP_204_NO_CONTENT, dependencies=[Depends(validate_token)]
)
async def users_delete(client_id: UUID):
    user = await ClientModel.get_or_404(client_id)
    await user.delete()


def include_router(app):
    app.include_router(router)
