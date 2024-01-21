from sqlalchemy.orm import Session
from fastapi import HTTPException
from DataBase import Menu, Submenu, Dish


def get_menu_data(db: Session, menu_id: str):
    db_menu = db.query(Menu).filter(Menu.id == menu_id).first()
    if db_menu:
        return \
            {"id": db_menu.id,
                "title": db_menu.title,
                "description": db_menu.description,
                "submenus_count": db.query(Submenu, Menu).join(Submenu, Submenu.menu_id==db_menu.id).count(),
                "dishes_count": db.query(Submenu, Menu).join(Submenu, Submenu.menu_id==db_menu.id).join(Dish, Dish.submenu_id==Submenu.id).count()
            }
    else:
        raise HTTPException(status_code=404, detail="menu not found")

def get_all_menus(db: Session):
    menus = db.query(Menu).all()
    return [
        {
            "id": menu.id,
            "title": menu.title,
            "description": menu.description,
            "submenus_count": db.query(Submenu, Menu).join(Submenu, Submenu.menu_id==menu.id).count(),
            "dishes_count": db.query(Submenu, Menu).join(Submenu, Submenu.menu_id==menu.id).join(Dish, Dish.submenu_id==Submenu.id).count()
        }
        for menu in menus
    ]


def create_menu(db: Session, menu_title: str, description: str):
    db_menu = Menu(title=menu_title, description=description)
    db.add(db_menu)
    db.commit()
    db.refresh(db_menu)
    return {
        "id": db_menu.id,
        'title': menu_title,
        'description': description,
        "submenus_count": 0,
        "dishes_count": 0
    }

def update_menu_data(db: Session, menu_id: str, new_title: str, new_description: str):
    db_menu = db.query(Menu).filter(Menu.id == menu_id).first()
    if db_menu:
        db_menu.title, db_menu.description = new_title, new_description
        db.commit()
        db.refresh(db_menu)
        return get_menu_data(db, menu_id=menu_id)
    else:
        return {'detail': 'menu not found'}

def delete_menu_data(db: Session, menu_id: str):
    db_menu = db.query(Menu).filter(Menu.id == menu_id).first()
    if db_menu:
        db.delete(db_menu)
        db.commit()
        return {
            "status": "true",
            "message": "The menu has been deleted"
        }
    else:
        raise {'detail': 'menu not found'}