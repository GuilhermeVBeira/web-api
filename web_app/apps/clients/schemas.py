from uuid import UUID

from pydantic import BaseModel, EmailStr, Field


class Client(BaseModel):
    id: UUID = ""
    email: EmailStr
    username: str = Field(..., min_length=6, max_length=64, description="The name that represents the client")

    class Config:
        orm_mode = True

    def __str__(self):
        return f"{self.id}, {self.username}, {self.email}"
