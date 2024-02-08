from application.core.cache_repository import CacheRepository
from fastapi import Depends, BackgroundTasks
from application.menus.crud_repository import MenuRepository
from application.menus.schemas import MenuCreate, MenuResponse
from sqlalchemy.exc import NoResultFound


class MenuService:
    def __init__(
        self, cacher: CacheRepository = Depends(), crud: MenuRepository = Depends()
    ) -> None:
        self.crud = crud
        self.cacher = cacher

    async def get_menu_by_id(
        self, menu_id: str, background_task: BackgroundTasks
    ) -> MenuResponse:
        cache = await self.cacher.get_menu_cache_by_id(menu_id=menu_id)
        if cache:
            return cache
        item = await self.crud.get_menu_data(menu_id=menu_id)
        background_task.add_task(
            self.cacher.create_menu_cache, menu_id=menu_id, item=item
        )
        return item

    async def get_all_menus(
        self, background_task: BackgroundTasks
    ) -> list[MenuResponse]:
        cache = await self.cacher.get_all_menu()
        if cache:
            return cache
        item = await self.crud.get_all_menus()
        background_task.add_task(self.cacher.set_all_menu_cache, item=item)
        return item

    async def get_menu_submenus_and_dishes_count(self, menu_id: str):
        item = await self.crud.get_submenu_and_dishes_count(menu_id=menu_id)
        if item:
            # await self.cacher.set_menu_submenus_and_dishes_count(
            #     menu_id=menu_id, item=item
            # )
            return item
        else:
            raise NoResultFound("Menu not found")

    async def create_menu(
        self, data: MenuCreate, background_task: BackgroundTasks
    ) -> MenuResponse:
        item = await self.crud.create_menu(data)
        menu_id = item.id
        background_task.add_task(
            self.cacher.create_menu_cache, menu_id=menu_id, item=item
        )
        background_task.add_task(self.cacher.delete_all_menu)
        return item

    async def update_menu(
        self, menu_id: str, data: MenuCreate, background_task: BackgroundTasks
    ) -> MenuResponse | dict:
        item = await self.crud.update_menu_data(menu_id=menu_id, data=data)
        background_task.add_task(self.cacher.delete_menu_cache, menu_id=menu_id)
        background_task.add_task(self.cacher.delete_all_menu)
        return item

    async def delete_menu(self, menu_id: str, background_task: BackgroundTasks) -> dict:
        item = await self.crud.delete_menu_data(menu_id=menu_id)
        background_task.add_task(self.cacher.delete_all_menu)
        background_task.add_task(self.cacher.delete_menu_cache, menu_id=menu_id)
        return item
