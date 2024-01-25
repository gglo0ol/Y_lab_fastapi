from pydantic import BaseModel


class MenuBase(BaseModel):
    title: str
    description: str


class MenuResponse(MenuBase):
    id: str
    title: str
    description: str
    submenus_count: int
    dishes_count: int


class MenuCreate(MenuBase):
    title: str
    description: str


class MenuUpdate(MenuBase):
    title: str
    description: str