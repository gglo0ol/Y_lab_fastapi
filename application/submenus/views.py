from typing import List
from sqlalchemy.orm import Session
from fastapi import Depends, APIRouter


from application.submenus.crud import (
    get_submenu_data,
    get_all_submenu_data,
    update_submenu_data,
    create_submenu,
    delete_submenu_data,
)
from application.submenus.schemas import SubmenuResponse, SubmenuCreate
from application.core.db import get_db


router = APIRouter(tags=["Submenus"], prefix="/api/v1/menus/{menu_id}/submenus")


@router.post("/", status_code=201, response_model=SubmenuResponse)
def create_submenu_endpoint(
    menu_id: str, data_in: SubmenuCreate, db: Session = Depends(get_db)
):
    return create_submenu(
        menu_id=menu_id,
        submenu_title=data_in.title,
        submenu_description=data_in.description,
        db=db,
    )


@router.get("/{submenu_id}", response_model=SubmenuResponse)
def get_submenu(menu_id: str, submenu_id: str, db: Session = Depends(get_db)):
    return get_submenu_data(submenu_id=submenu_id, menu_id=menu_id, db=db)


@router.get("/", response_model=List[SubmenuResponse])
def get_all_submenu(menu_id: str, db: Session = Depends(get_db)):
    return get_all_submenu_data(menu_id=menu_id, db=db)


@router.patch("/{submenu_id}", response_model=SubmenuResponse)
def update_submenu(
    menu_id: str, submenu_id: str, data_in: SubmenuCreate, db: Session = Depends(get_db)
):
    return update_submenu_data(
        submenu_id=submenu_id,
        new_submenu_title=data_in.title,
        new_submenu_description=data_in.description,
        db=db,
    )


@router.delete("/{submenu_id}")
def delete_submenu(menu_id: str, submenu_id: str, db: Session = Depends(get_db)):
    return delete_submenu_data(submenu_id=submenu_id, db=db)
