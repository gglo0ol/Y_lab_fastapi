import pickle

from core.config import (
    DISH_URL,
    DISHES_URL,
    MENU_URL,
    MENUS_URL,
    SUBMENU_URL,
    SUBMENUS_URL,
)
from core.db import get_redis
from dishes.schemas import DishResponse
from fastapi import Depends
from menus.schemas import MenuResponse
from redis.asyncio import Redis
from submenus.schemas import SubmenuResponse


class CacheRepository:
    def __init__(self, cacher: Redis = Depends(get_redis)) -> None:
        self.cacher = cacher

    async def set_all_menu_cache(self, item: list[MenuResponse]) -> None:
        await self.cacher.set(MENUS_URL, value=pickle.dumps(item))

    async def set_menu_cache(self, menu_id: str, item: MenuResponse) -> None:
        await self.cacher.set(
            name=MENU_URL.format(menu_id=menu_id), value=pickle.dumps(item), ex=300
        )

    async def set_menu_submenus_and_dishes_count(
        self, menu_id: str, item: dict
    ) -> None:
        await self.cacher.set(
            name=f"{menu_id}/submenus_and_dishes_count", value=pickle.dumps(item)
        )

    async def get_menu_submenus_and_dishes_count(self, menu_id: str) -> dict | None:
        cache = await self.cacher.get(name=f"{menu_id}/submenus_and_dishes_count")
        if cache:
            item = pickle.loads(cache)
            return item
        return None

    async def get_menu_cache_by_id(self, menu_id: str) -> MenuResponse | None:
        cache = await self.cacher.get(MENU_URL.format(menu_id=menu_id))
        if cache:
            item = pickle.loads(cache)
            return item
        return None

    async def get_all_menu(self) -> list[MenuResponse] | None:
        cache = await self.cacher.get(name=MENUS_URL)
        if cache:
            item = pickle.loads(cache)
            return item
        return None

    async def create_menu_cache(self, menu_id: str, item: MenuResponse | dict) -> None:
        await self.cacher.set(
            MENU_URL.format(menu_id=menu_id), value=pickle.dumps(item), ex=300
        )

    async def delete_menu_cache(self, menu_id: str) -> None:
        await self.cacher.delete(MENU_URL.format(menu_id=menu_id))

    async def delete_all_menu(self) -> None:
        await self.cacher.delete(MENUS_URL)

    async def set_submenu_cache(
        self, menu_id: str, submenu_id: str, item: SubmenuResponse | dict
    ) -> None:
        await self.cacher.set(
            name=SUBMENU_URL.format(menu_id=menu_id, submenu_id=submenu_id),
            value=pickle.dumps(item),
        )

    async def set_all_submenu(self, menu_id: str, item: list[SubmenuResponse]) -> None:
        await self.cacher.set(
            name=SUBMENUS_URL.format(menu_id=menu_id), value=pickle.dumps(item)
        )

    async def create_submenu(
        self, menu_id: str, submenu_id: str, item: SubmenuResponse
    ) -> None:
        data = pickle.dumps(item)
        await self.cacher.set(
            name=SUBMENU_URL.format(menu_id=menu_id, submenu_id=submenu_id), value=data
        )
        await self.delete_all_menu()
        await self.delete_menu_cache(menu_id=menu_id)

    async def get_submenu_by_id(
        self, menu_id: str, submenu_id: str
    ) -> SubmenuResponse | None:
        cache = await self.cacher.get(
            name=SUBMENU_URL.format(menu_id=menu_id, submenu_id=submenu_id)
        )
        if cache:
            item = pickle.loads(cache)
            return item
        return None

    async def get_all_submenus(self, menu_id: str) -> list[SubmenuResponse] | None:
        cache = await self.cacher.get(name=SUBMENUS_URL.format(menu_id=menu_id))
        if cache:
            item = pickle.loads(cache)
            return item
        return None

    async def delete_submenu_by_id(self, menu_id: str, submenu_id: str) -> None:
        await self.cacher.delete(
            SUBMENU_URL.format(menu_id=menu_id, submenu_id=submenu_id)
        )
        await self.delete_all_menu()
        await self.delete_menu_cache(menu_id=menu_id)

    async def delete_all_submenus(self, menu_id: str) -> None:
        await self.cacher.delete(SUBMENUS_URL.format(menu_id=menu_id))

    async def set_dish(
        self, menu_id: str, submenu_id: str, dish_id: str, data: DishResponse | dict
    ) -> None:
        item = pickle.dumps(data)
        await self.cacher.set(
            name=DISH_URL.format(
                menu_id=menu_id, submenu_id=submenu_id, dish_id=dish_id
            ),
            value=item,
        )
        await self.delete_all_menu()
        await self.delete_all_submenus(menu_id=menu_id)
        await self.delete_menu_cache(menu_id=menu_id)
        await self.delete_submenu_by_id(menu_id=menu_id, submenu_id=submenu_id)

    async def set_all_dishes(
        self, menu_id: str, submenu_id: str, item: list[DishResponse]
    ) -> None:
        data = pickle.dumps(item)
        await self.cacher.set(
            name=DISHES_URL.format(menu_id=menu_id, submenu_id=submenu_id), value=data
        )

    async def get_all_dishes(
        self, menu_id: str, submenu_id: str
    ) -> list[DishResponse] | None:
        cache = await self.cacher.get(
            name=DISHES_URL.format(menu_id=menu_id, submenu_id=submenu_id)
        )
        if cache:
            item = pickle.loads(cache)
            return item
        return None

    async def get_dish_by_id(
        self, menu_id: str, submenu_id: str, dish_id: str
    ) -> DishResponse | None:
        cache = await self.cacher.get(
            name=DISH_URL.format(
                menu_id=menu_id, submenu_id=submenu_id, dish_id=dish_id
            )
        )
        if cache:
            item = pickle.loads(cache)
            return item
        return None

    async def delete_dish_by_id(
        self, menu_id: str, submenu_id: str, dish_id: str
    ) -> None:
        await self.cacher.delete(
            DISH_URL.format(menu_id=menu_id, submenu_id=submenu_id, dish_id=dish_id)
        )
        await self.delete_all_menu()
        await self.delete_all_submenus(menu_id=menu_id)
        await self.delete_menu_cache(menu_id=menu_id)
        await self.delete_submenu_by_id(menu_id=menu_id, submenu_id=submenu_id)

    async def delete_all_dishes(self, menu_id: str, submenu_id: str) -> None:
        await self.cacher.delete(
            DISHES_URL.format(menu_id=menu_id, submenu_id=submenu_id)
        )
        await self.delete_all_menu()
        await self.delete_all_submenus(menu_id=menu_id)
