from pydantic import BaseModel
from uuid import UUID
from application.dishes.schemas import DishResponse
from application.submenus.schemas import SubmenuDishes


class MenuResponse(BaseModel):
    id: UUID
    title: str
    description: str
    submenus_count: int
    dishes_count: int


class MenuCreate(BaseModel):
    title: str
    description: str


class MenuSubmenuDishes(MenuCreate):
    id: UUID
    submenus: list[SubmenuDishes]
