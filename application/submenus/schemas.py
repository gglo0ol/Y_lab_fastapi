from pydantic import BaseModel


class SubmenuCreate(BaseModel):
    title: str
    description: str


class SubmenuResponse(BaseModel):
    id: str
    menu_id: str
    title: str
    description: str
    dishes_count: int
