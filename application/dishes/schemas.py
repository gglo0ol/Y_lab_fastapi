from pydantic import (
    BaseModel,
    field_validator,
    validator,
    ValidationInfo,
    field_validator,
)
from core.models.base import Dish
from uuid import UUID
from contextlib import contextmanager
from contextvars import ContextVar
from typing import Any, Dict, Iterator


class DishCreate(BaseModel):
    title: str
    description: str
    price: str
    discount: int


class DishResponse(BaseModel):
    id: UUID
    submenu_id: UUID
    title: str
    description: str
    price: str
    discount: int

    # @field_validator("price")
    # @classmethod
    # def apply_discount(cls, v: str, values: ValidationInfo) -> str:
    #     price = float(v.replace(",", "."))
    #     discount = values.data.get("discount")
    #     discounted_price = price - (price * discount / 100)
    #     return f"{discounted_price:.2f}"
