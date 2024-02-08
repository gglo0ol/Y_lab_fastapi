from pydantic import BaseModel
from uuid import UUID


class DishCreate(BaseModel):
    title: str
    description: str
    price: str


class DishResponse(BaseModel):
    id: UUID
    submenu_id: UUID
    title: str
    description: str
    price: str
