from typing import List
from sqlalchemy.orm import Session
from fastapi import Depends, APIRouter


from submenus.crud import (
    get_submenu_data,
    get_all_submenu_data,
    update_submenu_data,
    create_submenu,
    delete_submenu_data,
)
from submenus.schemas import SubmenuUpdate, SubmenuResponse, SubmenuCreate
from core.db import get_db


router = APIRouter(tags=["Submenus"])  # add prefix="/api/v1/menus/{menu_id}/submenus"


@router.post("/api/v1/menus/{menu_id}/submenus", status_code=201)
def create_submenu_endpoint(
    menu_id: str, data_in: SubmenuCreate, db: Session = Depends(get_db)
):
    return create_submenu(
        menu_id=menu_id,
        submenu_title=data_in.title,
        submenu_description=data_in.description,
        db=db,
    )


@router.get("/api/v1/menus/{menu_id}/submenus/{submenu_id}")
def get_submenu(menu_id: str, submenu_id: str, db: Session = Depends(get_db)):
    return get_submenu_data(submenu_id=submenu_id, menu_id=menu_id, db=db)


@router.get("/api/v1/menus/{menu_id}/submenus", response_model=List[SubmenuResponse])
def get_all_submenu(menu_id: str, db: Session = Depends(get_db)):
    return get_all_submenu_data(menu_id=menu_id, db=db)


@router.patch("/api/v1/menus/{menu_id}/submenus/{submenu_id}")
def update_submenu(
    menu_id: str, submenu_id: str, data_in: SubmenuCreate, db: Session = Depends(get_db)
):
    return update_submenu_data(
        submenu_id=submenu_id,
        new_submenu_title=data_in.title,
        new_submenu_description=data_in.description,
        db=db,
    )


@router.delete("/api/v1/menus/{menu_id}/submenus/{submenu_id}")
def delete_submenu(menu_id: str, submenu_id: str, db: Session = Depends(get_db)):
    return delete_submenu_data(submenu_id=submenu_id, db=db)
