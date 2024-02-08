from application.core.db import get_db
from application.core.models.base import Dish, Menu, Submenu
from fastapi import Depends
from application.menus.schemas import MenuCreate, MenuResponse, MenuSubmenuDishes
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.orm import selectinload
from typing import Sequence


class MenuRepository:
    def __init__(self, db: AsyncSession = Depends(get_db)) -> None:
        self.db = db

    async def get_menu_data(self, menu_id: str) -> MenuResponse:
        db_menu = (
            await self.db.execute(select(Menu).where(Menu.id == menu_id))
        ).scalar()
        result = await self.get_submenu_and_dishes_count(menu_id=menu_id)
        submenu_count, dishes_count = (
            result["submenu_count"],
            result["dishes_count"],
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
            raise NoResultFound("menu not found")

    async def get_submenu_and_dishes_count(self, menu_id: str):
        count_submenu_and_dishes = (
            select(
                Menu.id.label("menu_id"),
                func.count(func.distinct(Submenu.id)).label("submenu_id"),
                func.count(func.distinct(Dish.id)).label("dish_id"),
            )
            .where(Menu.id == menu_id)
            .join(Submenu, Menu.submenus)
            .outerjoin(Dish, Submenu.dishes)
            .group_by(Menu.id, Submenu.id)
            .subquery()
        )
        result = (
            await self.db.execute(
                select(
                    func.sum(count_submenu_and_dishes.c.submenu_id).label(
                        "submenu_count"
                    ),
                    func.sum(count_submenu_and_dishes.c.dish_id).label("dishes_count"),
                ).group_by(count_submenu_and_dishes.c.menu_id)
            )
        ).first()
        if result:
            submenu_count, dishes_count = (result.submenu_count, result.dishes_count)
        else:
            submenu_count, dishes_count = (0, 0)

        return {
            "menu_id": menu_id,
            "submenu_count": submenu_count,
            "dishes_count": dishes_count,
        }

    async def get_all_menus(self):
        db_menu = (await self.db.execute(select(Menu))).scalars()
        return [await self.get_menu_data(menu_id=menu.id) for menu in db_menu]

    async def create_menu(self, data: MenuCreate) -> MenuResponse:
        db_menu = Menu(title=data.title, description=data.description)
        self.db.add(db_menu)
        await self.db.commit()
        await self.db.refresh(db_menu)
        return await self.get_menu_data(menu_id=db_menu.id)

    async def update_menu_data(
        self, menu_id: str, data: MenuCreate
    ) -> MenuResponse | dict:
        db_menu = (
            await self.db.execute(select(Menu).where(Menu.id == menu_id))
        ).scalar()
        if db_menu:
            db_menu.title, db_menu.description = data.title, data.description
            await self.db.commit()
            await self.db.refresh(db_menu)
            return await self.get_menu_data(menu_id=menu_id)
        else:
            raise NoResultFound("Menu not found")

    async def delete_menu_data(self, menu_id: str) -> dict:
        db_menu = (
            await self.db.execute(select(Menu).where(Menu.id == menu_id))
        ).scalar()
        if db_menu:
            await self.db.delete(db_menu)
            await self.db.commit()
            return {"status": "true", "message": "The menu has been deleted"}
        else:
            raise NoResultFound("Menu not found")

    async def get_all_menu_and_submenu_and_dishes_data(self) -> Sequence[Menu]:
        result = (
            (
                await self.db.execute(
                    select(Menu).options(
                        selectinload(Menu.submenus).options(
                            selectinload(Submenu.dishes)
                        )
                    )
                )
            )
            .scalars()
            .fetchall()
        )
        return result
