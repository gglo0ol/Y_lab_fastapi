from pydantic import BaseModel
from uuid import UUID


class MenuResponse(BaseModel):
    id: UUID
    title: str
    description: str
    submenus_count: int
    dishes_count: int


class MenuCreate(BaseModel):
    title: str
    description: str
