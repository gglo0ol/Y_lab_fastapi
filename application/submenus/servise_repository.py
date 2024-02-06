from core.cache_repository import CacheRepository
from fastapi import Depends
from submenus.crud_repository import SubmenuRepository
from submenus.schemas import SubmenuCreate, SubmenuResponse


class SubmenuService:
    def __init__(
        self, cacher: CacheRepository = Depends(), crud: SubmenuRepository = Depends()
    ) -> None:
        self.cache = cacher
        self.crud = crud

    def get_submenu_by_id(self, menu_id: str, submenu_id: str) -> SubmenuResponse:
        cache = self.cache.get_submenu_by_id(menu_id=menu_id, submenu_id=submenu_id)
        if cache:
            return cache
        item = self.crud.get_submenu_data(menu_id=menu_id, submenu_id=submenu_id)
        self.cache.set_submenu_cache(menu_id=menu_id, submenu_id=submenu_id, item=item)
        return item

    def create_submenu(self, menu_id: str, data: SubmenuCreate) -> SubmenuResponse:
        item = self.crud.create_submenu(menu_id=menu_id, data=data)
        submenu_id = item.id
        self.cache.create_submenu(menu_id=menu_id, item=item, submenu_id=submenu_id)
        self.cache.delete_all_menu()
        self.cache.delete_all_submenus(menu_id=menu_id)
        return item

    def get_all_submenu(self, menu_id: str) -> list[SubmenuResponse]:
        cache = self.cache.get_all_submenus(menu_id=menu_id)
        if cache:
            return cache
        item = self.crud.get_all_submenu_data(menu_id=menu_id)
        self.cache.set_all_submenu(menu_id=menu_id, item=item)
        return item

    def update_submenu_by_id(
        self, menu_id: str, submenu_id: str, data: SubmenuCreate
    ) -> SubmenuResponse | dict:
        self.cache.delete_submenu_by_id(menu_id=menu_id, submenu_id=submenu_id)
        item = self.crud.update_submenu_data(submenu_id=submenu_id, data=data)
        self.cache.set_submenu_cache(menu_id=menu_id, submenu_id=submenu_id, item=item)
        self.cache.delete_all_submenus(menu_id=menu_id)
        self.cache.delete_all_menu()
        self.cache.delete_all_dishes(menu_id=menu_id, submenu_id=submenu_id)
        return item

    def delete_submenu_by_id(self, menu_id: str, submenu_id: str) -> dict:
        self.cache.delete_submenu_by_id(menu_id=menu_id, submenu_id=submenu_id)
        item = self.crud.delete_submenu_data(submenu_id=submenu_id)
        self.cache.delete_all_menu()
        self.cache.delete_all_submenus()
        self.cache.delete_all_dishes(menu_id=menu_id, submenu_id=submenu_id)
        return item
