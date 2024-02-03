from typing import List

from fastapi import Depends
from redis import Redis
import pickle

from core.db import get_redis
from menus.schemas import MenuResponse
from submenus.schemas import SubmenuResponse
from dishes.schemas import DishResponse, DishCreate
from core.config import (
    MENU_URL,
    MENUS_URL,
    SUBMENU_URL,
    SUBMENUS_URL,
    DISH_URL,
    DISHES_URL,
)


class CacheRepository:
    def __init__(self, cacher: Redis = Depends(get_redis)):
        self.cacher = cacher

    def set_all_menu_cache(self, item: List[MenuResponse]):
        self.cacher.set(MENUS_URL, value=pickle.dumps(item))

    def set_menu_cache(self, menu_id: str, item: MenuResponse):
        self.cacher.set(
            name=MENU_URL.format(menu_id=menu_id), value=pickle.dumps(item), ex=300
        )

    def set_menu_submenus_and_dishes_count(self, menu_id: str, item):
        self.cacher.set(
            name=f"{menu_id}/submenus_and_dishes_count", value=pickle.dumps(item)
        )

    def get_menu_submenus_and_dishes_count(self, menu_id: str):
        cache = self.cacher.get(name=f"{menu_id}/submenus_and_dishes_count")
        if cache:
            item = pickle.loads(cache)
            return item
        return None

    def get_menu_cache_by_id(self, menu_id: str):
        cache = self.cacher.get(MENU_URL.format(menu_id=menu_id))
        if cache:
            item = pickle.loads(cache)
            return item
        return None

    def get_all_menu(self):
        cache = self.cacher.get(name=MENUS_URL)
        if cache:
            item = pickle.loads(cache)
            return item
        return None

    def update_menu_cache(self, menu_id: str, item: MenuResponse):
        self.delete_menu_cache(menu_id=menu_id)
        self.create_menu_cache(menu_id=menu_id, item=item)

    def create_menu_cache(self, menu_id: str, item: MenuResponse):
        self.cacher.set(
            MENU_URL.format(menu_id=menu_id), value=pickle.dumps(item), ex=300
        )

    def delete_menu_cache(self, menu_id: id):
        self.cacher.delete(MENU_URL.format(menu_id=menu_id))

    def delete_all_menu(self):
        self.cacher.delete(MENUS_URL)

    def set_submenu_cache(self, menu_id: str, submenu_id: str, item: SubmenuResponse):
        self.cacher.set(
            name=SUBMENU_URL.format(menu_id=menu_id, submenu_id=submenu_id),
            value=pickle.dumps(item),
        )

    def set_all_submenu(self, menu_id: str, item: list[SubmenuResponse]):
        self.cacher.set(
            name=SUBMENUS_URL.format(menu_id=menu_id), value=pickle.dumps(item)
        )

    def create_submenu(self, menu_id: str, submenu_id: str, item: SubmenuResponse):
        data = pickle.dumps(item)
        self.cacher.set(
            name=SUBMENU_URL.format(menu_id=menu_id, submenu_id=submenu_id), value=data
        )
        self.delete_all_menu()
        self.delete_menu_cache(menu_id=menu_id)

    def get_submenu_by_id(self, menu_id: str, submenu_id: str):
        cache = self.cacher.get(
            name=SUBMENU_URL.format(menu_id=menu_id, submenu_id=submenu_id)
        )
        if cache:
            item = pickle.loads(cache)
            return item
        return None

    def get_all_submenus(self, menu_id):
        cache = self.cacher.get(name=SUBMENUS_URL.format(menu_id=menu_id))
        if cache:
            item = pickle.loads(cache)
            return item
        return None

    def update_submenu_by_id(
        self, menu_id: str, submenu_id: str, item: SubmenuResponse
    ):
        self.delete_submenu_by_id(menu_id=menu_id, submenu_id=submenu_id)
        self.set_submenu_cache(menu_id=menu_id, submenu_id=submenu_id, item=item)
        self.delete_all_menu()
        self.delete_menu_cache(menu_id=menu_id)

    def delete_submenu_by_id(self, menu_id: str, submenu_id: str):
        self.cacher.delete(SUBMENU_URL.format(menu_id=menu_id, submenu_id=submenu_id))
        self.delete_all_menu()
        self.delete_menu_cache(menu_id=menu_id)

    def delete_all_submenus(self, menu_id: str):
        self.cacher.delete(SUBMENUS_URL.format(menu_id=menu_id))

    def set_dish(self, menu_id: str, submenu_id: str, dish_id: str, data: DishResponse):
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

    def set_all_dishes(self, menu_id: str, submenu_id: str, item: DishResponse):
        data = pickle.dumps(item)
        self.cacher.set(
            name=DISHES_URL.format(menu_id=menu_id, submenu_id=submenu_id), value=data
        )

    def get_all_dishes(self, menu_id: str, submenu_id: str):
        self.cacher.get(name=DISHES_URL.format(menu_id=menu_id, submenu_id=submenu_id))

    def get_dish_by_id(self, menu_id: str, submenu_id: str, dish_id: str):
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
        self, menu_id: str, submenu_id: str, dish_id: str, item: DishResponse
    ):
        self.delete_dish_by_id(menu_id=menu_id, submenu_id=submenu_id, dish_id=dish_id)
        self.set_dish(
            menu_id=menu_id, submenu_id=submenu_id, dish_id=dish_id, data=item
        )
        self.delete_all_menu()
        self.delete_all_submenus(menu_id=menu_id)
        self.delete_menu_cache(menu_id=menu_id)
        self.delete_submenu_by_id(menu_id=menu_id, submenu_id=submenu_id)

    def delete_dish_by_id(self, menu_id: str, submenu_id: str, dish_id: str):
        self.cacher.delete(
            DISH_URL.format(menu_id=menu_id, submenu_id=submenu_id, dish_id=dish_id)
        )
        self.delete_all_menu()
        self.delete_all_submenus(menu_id=menu_id)
        self.delete_menu_cache(menu_id=menu_id)
        self.delete_submenu_by_id(menu_id=menu_id, submenu_id=submenu_id)

    def delete_all_dishes(self, menu_id: str, submenu_id: str):
        self.cacher.delete(DISHES_URL.format(menu_id=menu_id, submenu_id=submenu_id))
        self.delete_all_menu()
        self.delete_all_submenus(menu_id=menu_id)
