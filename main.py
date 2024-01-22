from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from typing import List


from DataBase import get_db
from schema.menus import (get_menu_data, get_all_menus, update_menu_data, delete_menu_data,
                          create_menu, MenuCreate, MenuUpdate, MenuResponse)
from schema.submenus import (get_submenu_data, get_all_submenu_data,
                             create_submenu, update_submenu_data, delete_submenu_data, SubmenuCreate, SubmenuResponse)
from schema.dishes import (get_dish_data, get_all_dishes_data, create_dish, DishResponse, DishCreate, update_dish_data,
                           delete_dish_data)

app = FastAPI()



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


@app.post("/api/v1/menus/{menu_id}/submenus", status_code=201)
def create_submenu_endpoint(menu_id: str, data_in: SubmenuCreate, db: Session = Depends(get_db)):
    return create_submenu(menu_id=menu_id, submenu_title=data_in.title, submenu_description=data_in.description, db=db)


@app.get("/api/v1/menus/{menu_id}/submenus/{submenu_id}")
def get_submenu(menu_id: str, submenu_id: str, db: Session = Depends(get_db)):
    return get_submenu_data(submenu_id=submenu_id, menu_id=menu_id, db=db)


@app.get("/api/v1/menus/{menu_id}/submenus", response_model=List[SubmenuResponse])
def get_all_submenu(menu_id: str, db: Session = Depends(get_db)):
    return get_all_submenu_data(menu_id=menu_id, db=db)

@app.patch("/api/v1/menus/{menu_id}/submenus/{submenu_id}")
def update_submenu(menu_id: str, submenu_id: str, data_in: SubmenuCreate, db: Session = Depends(get_db)):
    return update_submenu_data(submenu_id=submenu_id, new_submenu_title=data_in.title, new_submenu_description=data_in.description, db=db)


@app.delete("/api/v1/menus/{menu_id}/submenus/{submenu_id}")
def delete_submenu(menu_id: str, submenu_id: str, db: Session = Depends(get_db)):
    return delete_submenu_data(submenu_id=submenu_id, db=db)





@app.post("/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes", status_code=201)
def create_dish_endpoint(menu_id: str, submenu_id: str, data_in: DishCreate, db: Session = Depends(get_db)):
    return create_dish(submenu_id=submenu_id, dish_title=data_in.title, dish_description=data_in.description, dish_price=data_in.price, db=db)


@app.get("/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}")
def get_dish(menu_id: str, submenu_id: str, dish_id: str, db: Session = Depends(get_db)):
    return get_dish_data(submenu_id=submenu_id, dish_id=dish_id, db=db)


@app.patch("/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}", response_model=DishResponse)
def update_dish(menu_id: str, submenu_id: str, dish_id: str, data_in: DishResponse, db: Session = Depends(get_db)):
    return update_dish_data(dish_id=dish_id, new_dish_title=data_in.title, new_dish_description=data_in.description,
                            new_dish_price= data_in.price, db=db)


@app.delete("/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}")
def delete_dish(menu_id: str, submenu_id: str, dish_id: str, db: Session = Depends(get_db)):
    return delete_dish_data(dish_id=dish_id, db=db)




@app.get("/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes")
def get_all_dishes(menu_id: str, submenu_id: str, db: Session = Depends(get_db)):
    print(menu_id, submenu_id)
    return get_all_dishes_data(submenu_id=submenu_id, db=db)


if __name__ == "__main__":
    # DataBase.delete_entire_database()
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000)
