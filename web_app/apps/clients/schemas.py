from typing import List
from uuid import UUID

from pydantic import BaseModel, EmailStr, Field


class FavoriteProductRequest(BaseModel):
    id: UUID = ""

    class Config:
        orm_mode = True


class FavoriteProduct(FavoriteProductRequest):
    price: str
    image: str
    brand: str
    title: str


class Client(BaseModel):
    id: UUID = ""
    email: EmailStr
    username: str = Field(..., min_length=6, max_length=64, description="The name that represents the client")

    class Config:
        orm_mode = True

    def __str__(self):
        return f"{self.id}, {self.username}, {self.email}"


class ClientProductsRequest(Client):
    favorite_products: List[FavoriteProductRequest] = []


class ClientProductsResponse(ClientProductsRequest):
    id: UUID = ""
    favorite_products: List[FavoriteProduct] = []
