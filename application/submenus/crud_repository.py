from core.db import get_db
from core.models.base import Dish, Submenu
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm.exc import NoResultFound
from submenus.schemas import SubmenuCreate, SubmenuResponse, SubmenuCreateWithId
from sqlalchemy import func, select


class SubmenuRepository:
    def __init__(self, db: AsyncSession = Depends(get_db)) -> None:
        self.db = db

    async def get_submenu_data(self, submenu_id: str, menu_id: str):
        db_submenu = (
            await self.db.execute(select(Submenu).where(Submenu.id == submenu_id))
        ).scalar()
        if db_submenu:
            dishes_count = (
                (
                    await self.db.execute(
                        select(func.count(Submenu.id))
                        .where(Submenu.id == submenu_id)
                        .join(Dish, Submenu.id == Dish.submenu_id)
                    )
                )
                .first()
                .count
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
            raise NoResultFound("submenu not found")

    async def get_all_submenu_data(self, menu_id: str) -> list[SubmenuResponse]:
        db_submenu = (
            await self.db.execute(select(Submenu).filter(Submenu.menu_id == menu_id))
        ).scalars()
        return [
            await self.get_submenu_data(submenu_id=submenu.id, menu_id=menu_id)
            for submenu in db_submenu
        ]

    async def create_submenu(
        self, menu_id: str, data: SubmenuCreateWithId
    ) -> SubmenuResponse:
        db_submenu = Submenu(
            menu_id=menu_id,
            title=data.title,
            description=data.description,
            id=data.id,
        )
        self.db.add(db_submenu)
        await self.db.commit()
        await self.db.refresh(db_submenu)
        return await self.get_submenu_data(submenu_id=db_submenu.id, menu_id=menu_id)

    async def update_submenu_data(
        self,
        submenu_id: str,
        data: SubmenuCreate,
    ) -> SubmenuResponse | dict:
        db_submenu = (
            await self.db.execute(select(Submenu).filter(Submenu.id == submenu_id))
        ).scalar()
        if db_submenu:
            db_submenu.title, db_submenu.description = (
                data.title,
                data.description,
            )
            self.db.add(db_submenu)
            await self.db.commit()
            await self.db.refresh(db_submenu)
            return await self.get_submenu_data(
                submenu_id=db_submenu.id, menu_id=db_submenu.menu_id
            )
        else:
            raise NoResultFound("submenu not found")

    async def delete_submenu_data(self, submenu_id: str) -> dict:
        db_submenu = (
            await self.db.execute(select(Submenu).filter(Submenu.id == submenu_id))
        ).scalar()
        if db_submenu:
            await self.db.delete(db_submenu)
            await self.db.commit()
            return {"status": "true", "message": "The submenu has been deleted"}
        else:
            raise NoResultFound("submenu not found")
