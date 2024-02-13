from pydantic import (
    BaseModel,
    root_validator,
)
from core.models.base import Dish
from uuid import UUID


class DishCreate(BaseModel):
    title: str
    description: str
    price: str
    discount: int = 50


class DishCreateWithId(DishCreate):
    id: UUID | None = None


class DishResponse(BaseModel):
    id: UUID
    submenu_id: UUID
    title: str
    description: str
    price: str
    discount: int


class DishResponseRead(BaseModel):
    id: UUID
    submenu_id: UUID
    title: str
    description: str
    discount: int
    price: str

    @root_validator(pre=True)
    @classmethod
    def price_discount(cls, values: Dish) -> Dish:
        price = values.price
        price = float(price.replace(",", "."))
        discount = values.discount

        if price and discount:
            discounted_price = round((price * (100 - discount) / 100), 2)
            values.price = str(discounted_price)
        return values
