from fastapi import APIRouter, Depends, status, HTTPException
from web_app.apps.auth.authentication import validate_token
from web_app.apps.clients.schemas import Client
from web_app.apps.clients.models import Client as ClientModel
from web_app.main import db

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


def include_router(app):
    app.include_router(router)
