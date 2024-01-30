from typing import List

from sqlalchemy.orm import Session
from fastapi import Depends, APIRouter


from dishes.crud import (
    get_dish_data,
    get_all_dishes_data,
    create_dish,
    update_dish_data,
    delete_dish_data,
)
from dishes.schemas import DishCreate, DishResponse
from core.db import get_db

router = APIRouter(
    tags=["Dishes"], prefix="/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes"
)


@router.post("/", status_code=201, response_model=DishResponse)
def create_dish_endpoint(
    menu_id: str, submenu_id: str, data_in: DishCreate, db: Session = Depends(get_db)
):
    return create_dish(
        submenu_id=submenu_id,
        title=data_in.title,
        description=data_in.description,
        price=data_in.price,
        db=db,
    )


@router.get("/{dish_id}", response_model=DishResponse)
def get_dish(
    menu_id: str, submenu_id: str, dish_id: str, db: Session = Depends(get_db)
):
    return get_dish_data(submenu_id=submenu_id, dish_id=dish_id, db=db)


@router.patch("/{dish_id}", response_model=DishResponse)
def update_dish(
    menu_id: str,
    submenu_id: str,
    dish_id: str,
    data_in: DishCreate,
    db: Session = Depends(get_db),
):
    return update_dish_data(
        id=dish_id,
        title=data_in.title,
        description=data_in.description,
        price=data_in.price,
        db=db,
    )


@router.delete("/{dish_id}")
def delete_dish(
    menu_id: str, submenu_id: str, dish_id: str, db: Session = Depends(get_db)
):
    return delete_dish_data(dish_id=dish_id, db=db)


@router.get("/", response_model=List[DishResponse])
def get_all_dishes(menu_id: str, submenu_id: str, db: Session = Depends(get_db)):
    return get_all_dishes_data(submenu_id=submenu_id, db=db)
