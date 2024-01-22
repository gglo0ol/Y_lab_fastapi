from sqlalchemy.orm import Session
from fastapi import HTTPException
from DataBase import Submenu, Dish
from DataBase import BaseModel

class SubmenuCreate(BaseModel):

    title: str
    description: str

class SubmenuResponse(BaseModel):
    id: str
    menu_id: str
    title: str
    description: str
    dishes_count: int


def get_submenu_data(db: Session, submenu_id: str, menu_id: str):
    db_submenu = db.query(Submenu).filter(Submenu.id==submenu_id).first()
    if db_submenu:
        return {
            "id": submenu_id,
            "menu_id": menu_id,
            "title": db_submenu.title,
            "description": db_submenu.description,
            "dishes_count": db.query(Submenu, Dish).join(Dish, db_submenu.id==Dish.submenu_id).count()
        }
    else:
        # return {'detail': 'submenu not found'}
        raise HTTPException(status_code=404, detail="submenu not found")


def get_all_submenu_data(menu_id: str, db: Session):
    db_submenu = db.query(Submenu).filter(Submenu.menu_id==menu_id).all()
    return [
        get_submenu_data(db=db, submenu_id=submenu.id, menu_id=menu_id)
        for submenu in db_submenu
    ]


def create_submenu(menu_id: str, submenu_title: str, submenu_description: str, db: Session):
    db_submenu = Submenu(menu_id=menu_id, title=submenu_title, description=submenu_description)
    db.add(db_submenu)
    db.commit()
    db.refresh(db_submenu)
    return get_submenu_data(submenu_id=db_submenu.id, menu_id=menu_id, db=db)


def update_submenu_data(submenu_id: str, new_submenu_title: str, new_submenu_description: str, db: Session):
    db_submenu = db.query(Submenu).filter(Submenu.id==submenu_id).first()
    if db_submenu:
        db_submenu.title, db_submenu.description = new_submenu_title, new_submenu_description
        db.add(db_submenu)
        db.commit()
        db.refresh(db_submenu)
        return get_submenu_data(db, submenu_id=db_submenu.id, menu_id=db_submenu.menu_id)
    else:
        return {'detail': 'submenu not found'}


def delete_submenu_data(submenu_id: str, db: Session):
    db_submenu = db.query(Submenu).filter(Submenu.id==submenu_id).first()
    if db_submenu:
        db.delete(db_submenu)
        db.commit()
        return {
            "status": "true",
            "message": "The submenu has been deleted"
        }
    else:
        return {"details": "menu not found"}
