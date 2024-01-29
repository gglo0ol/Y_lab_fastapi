from fastapi import HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func


from core.models.base import Menu, Submenu, Dish


def get_menu_data(db: Session, menu_id: str):
    db_menu = db.query(Menu).filter(Menu.id == menu_id).first()
    count_submenu_and_dishes = (
        db.query(
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
        db.query(
            func.sum(count_submenu_and_dishes.c.sub_id).label("submenus"),
            func.sum(count_submenu_and_dishes.c.dish_id).label("dishes"),
        )
        .group_by(count_submenu_and_dishes.c.menu_id)
        .first()
    )
    submenu_count, dishes_count = result or (0, 0)

    if db_menu:
        return {
            "id": db_menu.id,
            "title": db_menu.title,
            "description": db_menu.description,
            "submenus_count": submenu_count,
            "dishes_count": dishes_count,
        }
    else:
        raise HTTPException(status_code=404, detail="menu not found")


def get_all_menus(db: Session):
    db_menu = db.query(Menu).all()
    return [get_menu_data(menu_id=menu.id, db=db) for menu in db_menu]


def create_menu(db: Session, menu_title: str, description: str):
    db_menu = Menu(title=menu_title, description=description)
    db.add(db_menu)
    db.commit()
    db.refresh(db_menu)
    return {
        "id": db_menu.id,
        "title": menu_title,
        "description": description,
        "submenus_count": 0,
        "dishes_count": 0,
    }


def update_menu_data(db: Session, menu_id: str, new_title: str, new_description: str):
    db_menu = db.query(Menu).filter(Menu.id == menu_id).first()
    if db_menu:
        db_menu.title, db_menu.description = new_title, new_description
        db.commit()
        db.refresh(db_menu)
        return get_menu_data(db, menu_id=menu_id)
    else:
        return {"detail": "menu not found"}


def delete_menu_data(db: Session, menu_id: str):
    db_menu = db.query(Menu).filter(Menu.id == menu_id).first()
    if db_menu:
        db.delete(db_menu)
        db.commit()
        return {"status": "true", "message": "The menu has been deleted"}
    else:
        return {"detail": "menu not found"}
