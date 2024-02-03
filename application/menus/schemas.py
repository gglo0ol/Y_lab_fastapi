from pydantic import BaseModel


class MenuResponse(BaseModel):
    id: str
    title: str
    description: str
    submenus_count: int
    dishes_count: int


class MenuCreate(BaseModel):
    title: str
    description: str
