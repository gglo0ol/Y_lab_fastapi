import pickle

from fastapi import Depends

from submenus.crud_repository import SubmenuRepository
from submenus.schemas import SubmenuCreate
from core.cache_repository import CacheRepository


class SubmenuService:
    def __init__(
        self, cacher: CacheRepository = Depends(), crud: SubmenuRepository = Depends()
    ):
        self.cache = cacher
        self.crud = crud

    def get_submenu_by_id(self, menu_id: str, submenu_id: str):
        cache = self.cache.get_submenu_by_id(menu_id=menu_id, submenu_id=submenu_id)
        if cache:
            return cache
        item = self.crud.get_submenu_data(menu_id=menu_id, submenu_id=submenu_id)
        self.cache.set_submenu_cache(menu_id=menu_id, submenu_id=submenu_id, item=item)
        return item

    def create_submenu(self, menu_id: str, data: SubmenuCreate):
        item = self.crud.create_submenu(menu_id=menu_id, data=data)
        submenu_id = item.id
        self.cache.create_submenu(menu_id=menu_id, item=item, submenu_id=submenu_id)
        self.update_all_submenu(menu_id=menu_id)
        return item

    def get_all_submenu(self, menu_id: str):
        cache = self.cache.get_all_submenus(menu_id=menu_id)
        if cache:
            return cache
        item = self.crud.get_all_submenu_data(menu_id=menu_id)
        self.cache.set_all_menu_cache(item=item)
        return item

    def update_submenu_by_id(self, menu_id: str, submenu_id: str, data: SubmenuCreate):
        self.cache.delete_submenu_by_id(menu_id=menu_id, submenu_id=submenu_id)
        item = self.crud.update_submenu_data(submenu_id=submenu_id, data=data)
        self.cache.set_submenu_cache(menu_id=menu_id, submenu_id=submenu_id, item=item)
        self.update_all_submenu(menu_id=menu_id)
        return item

    def delete_submenu_by_id(self, menu_id: str, submenu_id: str):
        self.cache.delete_submenu_by_id(menu_id=menu_id, submenu_id=submenu_id)
        item = self.crud.delete_submenu_data(submenu_id=submenu_id)
        self.update_all_submenu(menu_id=menu_id)
        return item

    def update_all_submenu(self, menu_id: str):
        self.cache.delete_all_submenus(menu_id=menu_id)
        item = self.crud.get_all_submenu_data(menu_id=menu_id)
        self.cache.set_all_submenu(menu_id=menu_id, item=item)
