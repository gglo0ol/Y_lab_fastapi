from pydantic import BaseModel
from uuid import UUID


class SubmenuCreate(BaseModel):
    title: str
    description: str


class SubmenuResponse(BaseModel):
    id: UUID
    menu_id: UUID
    title: str
    description: str
    dishes_count: int
