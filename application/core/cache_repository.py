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
from redis import Redis
from submenus.schemas import SubmenuResponse


class CacheRepository:
    def __init__(self, cacher: Redis = Depends(get_redis)) -> None:
        self.cacher = cacher

    def set_all_menu_cache(self, item: list[MenuResponse]) -> None:
        self.cacher.set(MENUS_URL, value=pickle.dumps(item))

    def set_menu_cache(self, menu_id: str, item: MenuResponse) -> None:
        self.cacher.set(
            name=MENU_URL.format(menu_id=menu_id), value=pickle.dumps(item), ex=300
        )

    def set_menu_submenus_and_dishes_count(self, menu_id: str, item) -> None:
        self.cacher.set(
            name=f"{menu_id}/submenus_and_dishes_count", value=pickle.dumps(item)
        )

    def get_menu_submenus_and_dishes_count(self, menu_id: str) -> dict | None:
        cache = self.cacher.get(name=f"{menu_id}/submenus_and_dishes_count")
        if cache:
            item = pickle.loads(cache)
            return item
        return None

    def get_menu_cache_by_id(self, menu_id: str) -> MenuResponse | None:
        cache = self.cacher.get(MENU_URL.format(menu_id=menu_id))
        if cache:
            item = pickle.loads(cache)
            return item
        return None

    def get_all_menu(self) -> list[MenuResponse] | None:
        cache = self.cacher.get(name=MENUS_URL)
        if cache:
            item = pickle.loads(cache)
            return item
        return None

    def update_menu_cache(self, menu_id: str, item: MenuResponse | dict) -> None:
        self.delete_menu_cache(menu_id=menu_id)
        self.create_menu_cache(menu_id=menu_id, item=item)

    def create_menu_cache(self, menu_id: str, item: MenuResponse | dict) -> None:
        self.cacher.set(
            MENU_URL.format(menu_id=menu_id), value=pickle.dumps(item), ex=300
        )

    def delete_menu_cache(self, menu_id: str) -> None:
        self.cacher.delete(MENU_URL.format(menu_id=menu_id))

    def delete_all_menu(self) -> None:
        self.cacher.delete(MENUS_URL)

    def set_submenu_cache(
        self, menu_id: str, submenu_id: str, item: SubmenuResponse | dict
    ) -> None:
        self.cacher.set(
            name=SUBMENU_URL.format(menu_id=menu_id, submenu_id=submenu_id),
            value=pickle.dumps(item),
        )

    def set_all_submenu(self, menu_id: str, item: list[SubmenuResponse]) -> None:
        self.cacher.set(
            name=SUBMENUS_URL.format(menu_id=menu_id), value=pickle.dumps(item)
        )

    def create_submenu(
        self, menu_id: str, submenu_id: str, item: SubmenuResponse
    ) -> None:
        data = pickle.dumps(item)
        self.cacher.set(
            name=SUBMENU_URL.format(menu_id=menu_id, submenu_id=submenu_id), value=data
        )
        self.delete_all_menu()
        self.delete_menu_cache(menu_id=menu_id)

    def get_submenu_by_id(
        self, menu_id: str, submenu_id: str
    ) -> SubmenuResponse | None:
        cache = self.cacher.get(
            name=SUBMENU_URL.format(menu_id=menu_id, submenu_id=submenu_id)
        )
        if cache:
            item = pickle.loads(cache)
            return item
        return None

    def get_all_submenus(self, menu_id) -> list[SubmenuResponse] | None:
        cache = self.cacher.get(name=SUBMENUS_URL.format(menu_id=menu_id))
        if cache:
            item = pickle.loads(cache)
            return item
        return None

    def update_submenu_by_id(
        self, menu_id: str, submenu_id: str, item: SubmenuResponse
    ) -> None:
        self.delete_submenu_by_id(menu_id=menu_id, submenu_id=submenu_id)
        self.set_submenu_cache(menu_id=menu_id, submenu_id=submenu_id, item=item)
        self.delete_all_menu()
        self.delete_menu_cache(menu_id=menu_id)

    def delete_submenu_by_id(self, menu_id: str, submenu_id: str) -> None:
        self.cacher.delete(SUBMENU_URL.format(menu_id=menu_id, submenu_id=submenu_id))
        self.delete_all_menu()
        self.delete_menu_cache(menu_id=menu_id)

    def delete_all_submenus(self, menu_id: str) -> None:
        self.cacher.delete(SUBMENUS_URL.format(menu_id=menu_id))

    def set_dish(
        self, menu_id: str, submenu_id: str, dish_id: str, data: DishResponse | dict
    ) -> None:
        item = pickle.dumps(data)
        self.cacher.set(
            name=DISH_URL.format(
                menu_id=menu_id, submenu_id=submenu_id, dish_id=dish_id
            ),
            value=item,
        )
        self.delete_all_menu()
        self.delete_all_submenus(menu_id=menu_id)
        self.delete_menu_cache(menu_id=menu_id)
        self.delete_submenu_by_id(menu_id=menu_id, submenu_id=submenu_id)

    def set_all_dishes(
        self, menu_id: str, submenu_id: str, item: list[DishResponse]
    ) -> None:
        data = pickle.dumps(item)
        self.cacher.set(
            name=DISHES_URL.format(menu_id=menu_id, submenu_id=submenu_id), value=data
        )

    def get_all_dishes(
        self, menu_id: str, submenu_id: str
    ) -> list[DishResponse] | None:
        cache = self.cacher.get(
            name=DISHES_URL.format(menu_id=menu_id, submenu_id=submenu_id)
        )
        if cache:
            item = pickle.loads(cache)
            return item
        return None

    def get_dish_by_id(
        self, menu_id: str, submenu_id: str, dish_id: str
    ) -> DishResponse | None:
        cache = self.cacher.get(
            name=DISH_URL.format(
                menu_id=menu_id, submenu_id=submenu_id, dish_id=dish_id
            )
        )
        if cache:
            item = pickle.loads(cache)
            return item
        return None

    def update_dish_by_id(
        self, menu_id: str, submenu_id: str, dish_id: str, item: DishResponse | dict
    ) -> None:
        self.delete_dish_by_id(menu_id=menu_id, submenu_id=submenu_id, dish_id=dish_id)
        self.set_dish(
            menu_id=menu_id, submenu_id=submenu_id, dish_id=dish_id, data=item
        )
        self.delete_all_menu()
        self.delete_all_submenus(menu_id=menu_id)
        self.delete_menu_cache(menu_id=menu_id)
        self.delete_submenu_by_id(menu_id=menu_id, submenu_id=submenu_id)

    def delete_dish_by_id(self, menu_id: str, submenu_id: str, dish_id: str) -> None:
        self.cacher.delete(
            DISH_URL.format(menu_id=menu_id, submenu_id=submenu_id, dish_id=dish_id)
        )
        self.delete_all_menu()
        self.delete_all_submenus(menu_id=menu_id)
        self.delete_menu_cache(menu_id=menu_id)
        self.delete_submenu_by_id(menu_id=menu_id, submenu_id=submenu_id)

    def delete_all_dishes(self, menu_id: str, submenu_id: str) -> None:
        self.cacher.delete(DISHES_URL.format(menu_id=menu_id, submenu_id=submenu_id))
        self.delete_all_menu()
        self.delete_all_submenus(menu_id=menu_id)
