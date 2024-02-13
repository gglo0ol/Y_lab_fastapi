from pydantic import BaseModel
from uuid import UUID
from dishes.schemas import DishResponseRead


class SubmenuCreate(BaseModel):
    title: str
    description: str


class SubmenuCreateWithId(SubmenuCreate):
    id: UUID | None = None


class SubmenuResponse(BaseModel):
    id: UUID
    menu_id: UUID
    title: str
    description: str
    dishes_count: int


class SubmenuDishes(SubmenuCreate):
    id: UUID
    dishes: list[DishResponseRead]
