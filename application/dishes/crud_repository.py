from core.db import get_db
from core.models.base import Dish
from dishes.schemas import DishCreate, DishCreateWithId
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy import select


class DishesRepository:
    def __init__(self, db: AsyncSession = Depends(get_db)) -> None:
        self.db = db

    async def create_dish(
        self,
        submenu_id: str,
        data: DishCreateWithId,
    ) -> Dish:
        db_dish = Dish(
            submenu_id=submenu_id,
            title=data.title,
            description=data.description,
            price=data.price,
            discount=data.discount,
            id=data.id,
        )
        self.db.add(db_dish)
        await self.db.commit()
        await self.db.refresh(db_dish)
        return await self.get_dish_data(submenu_id=submenu_id, dish_id=db_dish.id)

    async def get_dish_data(self, submenu_id: str, dish_id: str) -> Dish:
        db_dish = (
            await self.db.execute(
                select(Dish).where(Dish.submenu_id == submenu_id, Dish.id == dish_id)
            )
        ).scalar()

        if db_dish:
            return db_dish
        else:
            raise NoResultFound("dish not found")

    async def get_all_dishes_data(self, submenu_id: str) -> list[Dish]:
        db_dish = (
            await self.db.execute(select(Dish).where(Dish.submenu_id == submenu_id))
        ).scalars()
        return [
            await self.get_dish_data(dish_id=dish.id, submenu_id=dish.submenu_id)
            for dish in db_dish
        ]

    async def update_dish_data(
        self,
        dish_id: str,
        data: DishCreate | dict,
    ) -> Dish | dict:
        db_dish = (
            await self.db.execute(select(Dish).where(Dish.id == dish_id))
        ).scalar()
        if db_dish:
            db_dish.title, db_dish.description, db_dish.price, db_dish.discount = (
                data.title,
                data.description,
                data.price,
                data.discount,
            )
            self.db.add(db_dish)
            await self.db.commit()
            await self.db.refresh(db_dish)
            return await self.get_dish_data(
                submenu_id=db_dish.submenu_id, dish_id=db_dish.id
            )
        else:
            raise NoResultFound("dish not found")

    async def delete_dish_data(self, dish_id: str) -> dict:
        db_dish = (
            await self.db.execute(select(Dish).filter(Dish.id == dish_id))
        ).scalar()
        if db_dish:
            await self.db.delete(db_dish)
            await self.db.commit()
            return {"status": "true", "message": "The dish has been deleted"}
        else:
            raise NoResultFound("dish not found")
