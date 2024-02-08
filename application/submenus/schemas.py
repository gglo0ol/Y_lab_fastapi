from pydantic import BaseModel
from uuid import UUID
from application.dishes.schemas import DishResponse


class SubmenuCreate(BaseModel):
    title: str
    description: str


class SubmenuResponse(BaseModel):
    id: UUID
    menu_id: UUID
    title: str
    description: str
    dishes_count: int


class SubmenuDishes(SubmenuCreate):
    id: UUID
    dishes: list[DishResponse]
