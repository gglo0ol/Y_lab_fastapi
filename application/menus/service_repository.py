from core.cache_repository import CacheRepository
from fastapi import Depends
from menus.crud_repository import MenuRepository
from menus.schemas import MenuCreate, MenuResponse


class MenuService:
    def __init__(
        self, cacher: CacheRepository = Depends(), crud: MenuRepository = Depends()
    ) -> None:
        self.crud = crud
        self.cacher = cacher

    def get_menu_by_id(self, menu_id: str) -> MenuResponse:
        cache = self.cacher.get_menu_cache_by_id(menu_id=menu_id)
        if cache:
            return cache
        item = self.crud.get_menu_data(menu_id=menu_id)
        self.cacher.create_menu_cache(menu_id=menu_id, item=item)
        return item

    def get_all_menus(self) -> list[MenuResponse]:
        cache = self.cacher.get_all_menu()
        if cache:
            return cache
        item = self.crud.get_all_menus()
        self.cacher.set_all_menu_cache(item)
        return item

    def get_menu_submenus_and_dishes_count(self, menu_id: str) -> dict:
        item = self.crud.get_submenu_and_dishes_count(menu_id=menu_id)
        self.cacher.set_menu_submenus_and_dishes_count(menu_id=menu_id, item=item)
        return item

    def create_menu(self, data: MenuCreate) -> MenuResponse:
        item = self.crud.create_menu(data)
        menu_id = item.id
        self.cacher.create_menu_cache(menu_id=menu_id, item=item)
        self.cacher.delete_all_menu()
        return item

    def update_menu(self, menu_id: str, data: MenuCreate) -> MenuResponse | dict:
        item = self.crud.update_menu_data(menu_id=menu_id, data=data)
        self.cacher.delete_menu_cache(menu_id=menu_id)
        self.cacher.delete_all_menu()
        return item

    def delete_menu(self, menu_id: str) -> dict:
        self.cacher.delete_menu_cache(menu_id=menu_id)
        item = self.crud.delete_menu_data(menu_id=menu_id)
        self.cacher.delete_all_menu()
        return item
