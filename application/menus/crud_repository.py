from fastapi import HTTPException, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func


from core.models.base import Menu, Submenu, Dish
from core.db import get_db
from menus.schemas import MenuResponse, MenuCreate


class MenuRepository:
    def __init__(self, db: Session = Depends(get_db)):
        self.db = db

    def get_menu_data(self, menu_id: str):
        db_menu = self.db.query(Menu).filter(Menu.id == menu_id).first()
        result = self.get_submenu_and_dishes_count(menu_id=menu_id)
        submenu_count, dishes_count = (
            result["submenu_count"],
            result["dishes_count"],
        ) or (
            0,
            0,
        )

        if db_menu:
            data = {
                "id": db_menu.id,
                "title": db_menu.title,
                "description": db_menu.description,
                "submenus_count": submenu_count,
                "dishes_count": dishes_count,
            }
            return MenuResponse(**data)
        else:
            raise HTTPException(status_code=404, detail="menu not found")

    def get_submenu_and_dishes_count(self, menu_id: str):
        count_submenu_and_dishes = (
            self.db.query(
                Menu.id.label("menu_id"),
                func.count(func.distinct(Submenu.id)).label("sub_id"),
                func.count(func.distinct(Dish.id)).label("dish_id"),
            )
            .filter(Menu.id == menu_id)
            .join(Submenu, Menu.submenus)
            .outerjoin(Dish, Submenu.dishes)
            .group_by(Menu.id, Submenu.id)
            .subquery()
        )

        result = (
            self.db.query(
                func.sum(count_submenu_and_dishes.c.sub_id).label("submenus"),
                func.sum(count_submenu_and_dishes.c.dish_id).label("dishes"),
            )
            .group_by(count_submenu_and_dishes.c.menu_id)
            .first()
        )
        submenu_count, dishes_count = result or (0, 0)
        return {
            "menu_id": menu_id,
            "submenu_count": submenu_count,
            "dishes_count": dishes_count,
        }

    def get_all_menus(self):
        db_menu = self.db.query(Menu).all()
        return [self.get_menu_data(menu_id=menu.id) for menu in db_menu]

    def create_menu(self, data: MenuCreate):
        db_menu = Menu(title=data.title, description=data.description)
        self.db.add(db_menu)
        self.db.commit()
        self.db.refresh(db_menu)
        return self.get_menu_data(menu_id=db_menu.id)

    def update_menu_data(self, menu_id: str, data: MenuCreate):
        db_menu = self.db.query(Menu).filter(Menu.id == menu_id).first()
        if db_menu:
            db_menu.title, db_menu.description = data.title, data.description
            self.db.commit()
            self.db.refresh(db_menu)
            return self.get_menu_data(menu_id=menu_id)
        else:
            return {"detail": "menu not found"}

    def delete_menu_data(self, menu_id: str):
        db_menu = self.db.query(Menu).filter(Menu.id == menu_id).first()
        if db_menu:
            self.db.delete(db_menu)
            self.db.commit()
            return {"status": "true", "message": "The menu has been deleted"}
        else:
            return {"detail": "menu not found"}
