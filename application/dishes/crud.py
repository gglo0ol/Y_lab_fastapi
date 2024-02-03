# from sqlalchemy.orm import Session
# from fastapi import HTTPException
#
#
# from core.models.base import Dish
#
#
# def create_dish(
#     submenu_id: str,
#     title: str,
#     description: str,
#     price: str,
#     db: Session,
# ):
#     db_dish = Dish(
#         submenu_id=submenu_id,
#         title=title,
#         description=description,
#         price=price,
#     )
#     db.add(db_dish)
#     db.commit()
#     db.refresh(db_dish)
#     return get_dish_data(submenu_id=submenu_id, dish_id=db_dish.id, db=db)
#
#
# def get_dish_data(db: Session, submenu_id: str, dish_id: str):
#     db_dish = (
#         db.query(Dish).filter(Dish.submenu_id == submenu_id, Dish.id == dish_id).first()
#     )
#
#     if db_dish:
#         return {
#             "id": db_dish.id,
#             "submenu_id": db_dish.submenu_id,
#             "title": db_dish.title,
#             "description": db_dish.description,
#             "price": db_dish.price,
#         }
#     else:
#         raise HTTPException(status_code=404, detail="dish not found")
#
#
# def get_all_dishes_data(db: Session, submenu_id: str):
#     db_dish = db.query(Dish).filter(Dish.submenu_id == submenu_id).all()
#     return [
#         get_dish_data(dish_id=dish.id, submenu_id=dish.submenu_id, db=db)
#         for dish in db_dish
#     ]
#
#
# def update_dish_data(
#     id: str,
#     title: str,
#     description: str,
#     price: float,
#     db: Session,
# ):
#     db_dish = db.query(Dish).filter(Dish.id == id).first()
#     if db_dish:
#         db_dish.title, db_dish.description, db_dish.price = (
#             title,
#             description,
#             price,
#         )
#         db.add(db_dish)
#         db.commit()
#         db.refresh(db_dish)
#         return get_dish_data(db=db, submenu_id=db_dish.submenu_id, dish_id=db_dish.id)
#     else:
#         return {"detail": "dish not found"}
#
#
# def delete_dish_data(dish_id: str, db: Session):
#     db_dish = db.query(Dish).filter(Dish.id == dish_id).first()
#     if db_dish:
#         db.delete(db_dish)
#         db.commit()
#         return {"status": "true", "message": "The dish has been deleted"}
#     else:
#         return {"detail": "dish not found"}
