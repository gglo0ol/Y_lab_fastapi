from sqlalchemy.orm import Session
from fastapi import HTTPException, Depends

from core.models.base import Submenu, Dish
from core.cache_repository import CacheRepository
from core.db import get_db
from submenus.schemas import SubmenuCreate, SubmenuResponse


class SubmenuRepository:
    def __init__(self, db: Session = Depends(get_db)):
        self.db = db

    def get_submenu_data(self, submenu_id: str, menu_id: str):
        db_submenu = self.db.query(Submenu).filter(Submenu.id == submenu_id).first()
        if db_submenu:
            dishes_count = (
                self.db.query(Submenu)
                .filter(Submenu.id == submenu_id)
                .join(Dish, db_submenu.id == Dish.submenu_id)
                .count()
            )
            data = {
                "id": submenu_id,
                "menu_id": menu_id,
                "title": db_submenu.title,
                "description": db_submenu.description,
                "dishes_count": dishes_count,
            }
            return SubmenuResponse(**data)
        else:
            raise HTTPException(status_code=404, detail="submenu not found")

    def get_all_submenu_data(self, menu_id: str):
        db_submenu = self.db.query(Submenu).filter(Submenu.menu_id == menu_id).all()
        return [
            self.get_submenu_data(submenu_id=submenu.id, menu_id=menu_id)
            for submenu in db_submenu
        ]

    def create_submenu(self, menu_id: str, data: SubmenuCreate):
        db_submenu = Submenu(
            menu_id=menu_id, title=data.title, description=data.description
        )
        self.db.add(db_submenu)
        self.db.commit()
        self.db.refresh(db_submenu)
        return self.get_submenu_data(submenu_id=db_submenu.id, menu_id=menu_id)

    def update_submenu_data(
        self,
        submenu_id: str,
        data: SubmenuCreate,
    ):
        db_submenu = self.db.query(Submenu).filter(Submenu.id == submenu_id).first()
        if db_submenu:
            db_submenu.title, db_submenu.description = (
                data.title,
                data.description,
            )
            self.db.add(db_submenu)
            self.db.commit()
            self.db.refresh(db_submenu)
            return self.get_submenu_data(
                submenu_id=db_submenu.id, menu_id=db_submenu.menu_id
            )
        else:
            return {"detail": "submenu not found"}

    def delete_submenu_data(self, submenu_id: str):
        db_submenu = self.db.query(Submenu).filter(Submenu.id == submenu_id).first()
        if db_submenu:
            self.db.delete(db_submenu)
            self.db.commit()
            return {"status": "true", "message": "The submenu has been deleted"}
        else:
            return {"details": "menu not found"}
