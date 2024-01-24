from sqlalchemy.orm import Session
from fastapi import Depends, APIRouter


from dishes.crud import get_dish_data, get_all_dishes_data, create_dish, update_dish_data, delete_dish_data
from dishes.schemas import DishUpdate, DishCreate, DishResponse
from core.db import get_db

router = APIRouter(tags=["Dishes"])    # add prefix="/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes"

@router.post("/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes", status_code=201)
def create_dish_endpoint(menu_id: str, submenu_id: str, data_in: DishCreate, db: Session = Depends(get_db)):
    return create_dish(submenu_id=submenu_id, dish_title=data_in.title, dish_description=data_in.description,
                       dish_price=data_in.price, db=db)


@router.get("/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}")
def get_dish(menu_id: str, submenu_id: str, dish_id: str, db: Session = Depends(get_db)):
    return get_dish_data(submenu_id=submenu_id, dish_id=dish_id, db=db)


@router.patch("/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}", response_model=DishResponse)
def update_dish(menu_id: str, submenu_id: str, dish_id: str, data_in: DishResponse, db: Session = Depends(get_db)):
    return update_dish_data(dish_id=dish_id, new_dish_title=data_in.title, new_dish_description=data_in.description,
                            new_dish_price= data_in.price, db=db)


@router.delete("/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}")
def delete_dish(menu_id: str, submenu_id: str, dish_id: str, db: Session = Depends(get_db)):
    return delete_dish_data(dish_id=dish_id, db=db)


@router.get("/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes")
def get_all_dishes(menu_id: str, submenu_id: str, db: Session = Depends(get_db)):
    return get_all_dishes_data(submenu_id=submenu_id, db=db)