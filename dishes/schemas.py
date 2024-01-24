from pydantic import BaseModel

class DishCreate(BaseModel):
    title: str
    description: str
    price: str


class DishResponse(BaseModel):
    title: str
    description: str
    price: str


class DishUpdate(BaseModel):
    title: str
    description: str
    price: str
