from core.cache_repository import CacheRepository
from fastapi import Depends, BackgroundTasks
from submenus.crud_repository import SubmenuRepository
from submenus.schemas import SubmenuCreate, SubmenuResponse


class SubmenuService:
    def __init__(
        self, cacher: CacheRepository = Depends(), crud: SubmenuRepository = Depends()
    ) -> None:
        self.cache = cacher
        self.crud = crud

    async def get_submenu_by_id(
        self, menu_id: str, submenu_id: str, background_task: BackgroundTasks
    ) -> SubmenuResponse:
        cache = await self.cache.get_submenu_by_id(
            menu_id=menu_id, submenu_id=submenu_id
        )
        if cache:
            return cache
        item = await self.crud.get_submenu_data(menu_id=menu_id, submenu_id=submenu_id)
        background_task.add_task(
            self.cache.set_submenu_cache,
            menu_id=menu_id,
            submenu_id=submenu_id,
            item=item,
        )
        return item

    async def create_submenu(
        self, menu_id: str, data: SubmenuCreate, background_task: BackgroundTasks
    ) -> SubmenuResponse:
        item = await self.crud.create_submenu(menu_id=menu_id, data=data)
        submenu_id = item.id
        background_task.add_task(
            self.cache.create_submenu,
            menu_id=menu_id,
            submenu_id=submenu_id,
            item=item,
        )
        background_task.add_task(self.cache.delete_all_menu)
        background_task.add_task(self.cache.delete_all_submenus, menu_id=menu_id)
        background_task.add_task(self.cache.delete_menu_and_submenu_and_dishes)
        background_task.add_task(self.cache.delete_menu_cache, menu_id=menu_id)
        return item

    async def get_all_submenu(
        self, menu_id: str, background_task: BackgroundTasks
    ) -> list[SubmenuResponse]:
        cache = await self.cache.get_all_submenus(menu_id=menu_id)
        if cache:
            return cache
        item = await self.crud.get_all_submenu_data(menu_id=menu_id)
        background_task.add_task(self.cache.set_all_submenu, menu_id=menu_id, item=item)
        return item

    async def update_submenu_by_id(
        self,
        menu_id: str,
        submenu_id: str,
        data: SubmenuCreate,
        background_task: BackgroundTasks,
    ) -> SubmenuResponse | dict:
        background_task.add_task(
            self.cache.delete_submenu_by_id, menu_id=menu_id, submenu_id=submenu_id
        )
        item = await self.crud.update_submenu_data(submenu_id=submenu_id, data=data)
        background_task.add_task(
            self.cache.set_submenu_cache,
            menu_id=menu_id,
            submenu_id=submenu_id,
            item=item,
        )
        background_task.add_task(self.cache.delete_all_submenus, menu_id=menu_id)
        background_task.add_task(self.cache.delete_menu_and_submenu_and_dishes)
        return item

    async def delete_submenu_by_id(
        self, menu_id: str, submenu_id: str, background_task: BackgroundTasks
    ) -> dict:
        background_task.add_task(
            self.cache.delete_submenu_by_id, menu_id=menu_id, submenu_id=submenu_id
        )
        item = await self.crud.delete_submenu_data(submenu_id=submenu_id)
        background_task.add_task(self.cache.delete_all_menu)
        background_task.add_task(self.cache.delete_all_submenus, menu_id=menu_id)
        background_task.add_task(
            self.cache.delete_all_dishes, menu_id=menu_id, submenu_id=submenu_id
        )
        background_task.add_task(self.cache.delete_menu_and_submenu_and_dishes)
        background_task.add_task(self.cache.delete_menu_cache, menu_id=menu_id)
        return item
