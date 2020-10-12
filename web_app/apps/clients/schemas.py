from typing import List
from uuid import UUID

from pydantic import BaseModel, EmailStr, Field


class FavoriteProduct(BaseModel):
    id: UUID = ""
    price: str
    image: str
    brand: str
    title: str

    class Config:
        orm_mode = True


class ClientProducts(BaseModel):
    id: UUID = ""
    email: EmailStr
    favorite_products: List[FavoriteProduct] = []
    username: str = Field(..., min_length=6, max_length=64, description="The name that represents the client")

    class Config:
        orm_mode = True

    def __str__(self):
        return f"{self.id}, {self.username}, {self.email}"


class Client(BaseModel):
    id: UUID = ""
    email: EmailStr
    username: str = Field(..., min_length=6, max_length=64, description="The name that represents the client")

    class Config:
        orm_mode = True

    def __str__(self):
        return f"{self.id}, {self.username}, {self.email}"
