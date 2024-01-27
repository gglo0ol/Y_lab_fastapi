from typing import List

from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends


from menus.schemas import MenuUpdate, MenuResponse, MenuCreate
from menus.crud import (
    create_menu,
    get_all_menus,
    get_menu_data,
    update_menu_data,
    delete_menu_data,
)
from core.db import get_db

router = APIRouter(prefix="/api/v1/menus", tags=["Menu"])


@router.post("/", status_code=201)
def create_menu_endpoint(get_request: MenuCreate, db: Session = Depends(get_db)):
    return create_menu(db, get_request.title, get_request.description)


@router.get("/", response_model=List[MenuResponse])
def get_all_menus_endpoint(db: Session = Depends(get_db)):
    return get_all_menus(db)


@router.get("/{menu_id}/", response_model=MenuResponse)
def get_menu(menu_id: str, db: Session = Depends(get_db)):
    return get_menu_data(db, menu_id=menu_id)


@router.patch("/{menu_id}/")
def update_menu(menu_id: str, get_update: MenuUpdate, db: Session = Depends(get_db)):
    return update_menu_data(
        db,
        menu_id=menu_id,
        new_title=get_update.title,
        new_description=get_update.description,
    )


@router.delete("/{menu_id}/")
def delete_menu(menu_id: str, db: Session = Depends(get_db)):
    return delete_menu_data(db, menu_id=menu_id)
