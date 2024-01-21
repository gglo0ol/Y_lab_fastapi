from fastapi import FastAPI, Depends, status
from sqlalchemy.orm import declarative_base, Session, relationship
from typing import List
from DataBase import Menu, MenuBase, Submenu, UUID4, get_db
from schema.menus import get_menu_data, get_all_menus, update_menu_data, delete_menu_data, create_menu

app = FastAPI()

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

@app.post("/api/v1/menus", status_code=201)
def create_menu_endpoint(get_request: MenuCreate, db: Session = Depends(get_db)):
    return create_menu(db, get_request.title, get_request.description)


@app.get("/api/v1/menus", response_model=List[MenuResponse])
def get_all_menus_endpoint(db: Session = Depends(get_db)):
    return get_all_menus(db)

@app.get("/api/v1/menus/{menu_id}")
def get_menu(menu_id: str, db: Session = Depends(get_db)):
    return get_menu_data(db, menu_id=menu_id)


@app.patch("/api/v1/menus/{menu_id}")
def update_menu(menu_id: str, get_update: MenuUpdate, db: Session = Depends(get_db)):
    return update_menu_data(db, menu_id=menu_id, new_title=get_update.title, new_description=get_update.description)


@app.delete("/api/v1/menus/{menu_id}")
def delete_menu(menu_id: str, db: Session = Depends(get_db)):
    return delete_menu_data(db, menu_id=menu_id)


if __name__ == "__main__":
    # DataBase.delete_entire_database()
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000)
