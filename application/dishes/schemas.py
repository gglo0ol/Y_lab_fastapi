from pydantic import BaseModel


class DishCreate(BaseModel):
    title: str
    description: str
    price: str


class DishResponse(BaseModel):
    id: str
    submenu_id: str
    title: str
    description: str
    price: str
