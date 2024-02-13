from core.cache_repository import CacheRepository
from dishes.crud_repository import DishesRepository
from dishes.schemas import DishCreate, DishResponseRead
from core.models.base import Dish
from fastapi import Depends, BackgroundTasks


class DishesService:
    def __init__(
        self, cacher: CacheRepository = Depends(), crud: DishesRepository = Depends()
    ) -> None:
        self.cacher = cacher
        self.crud = crud

    async def get_dish(
        self,
        menu_id: str,
        submenu_id: str,
        dish_id: str,
        background_task: BackgroundTasks,
    ) -> Dish:
        cache = await self.cacher.get_dish_by_id(
            menu_id=menu_id, submenu_id=submenu_id, dish_id=dish_id
        )
        if cache:
            return cache
        item = await self.crud.get_dish_data(submenu_id=submenu_id, dish_id=dish_id)
        background_task.add_task(
            self.cacher.set_dish,
            menu_id=menu_id,
            submenu_id=submenu_id,
            dish_id=dish_id,
            data=item,
        )
        return item

    async def create_dish(
        self,
        menu_id: str,
        submenu_id: str,
        data: DishCreate,
        background_task: BackgroundTasks,
    ) -> Dish:
        item = await self.crud.create_dish(submenu_id=submenu_id, data=data)
        dish_id = item.id
        background_task.add_task(
            self.cacher.set_dish,
            menu_id=menu_id,
            submenu_id=submenu_id,
            dish_id=dish_id,
            data=item,
        )
        background_task.add_task(self.cacher.delete_all_menu)
        background_task.add_task(self.cacher.delete_all_submenus, menu_id=menu_id)
        background_task.add_task(
            self.cacher.delete_all_dishes, menu_id=menu_id, submenu_id=submenu_id
        )
        background_task.add_task(self.cacher.delete_menu_and_submenu_and_dishes)
        background_task.add_task(self.cacher.delete_menu_cache, menu_id=menu_id)
        background_task.add_task(
            self.cacher.delete_submenu_by_id, menu_id=menu_id, submenu_id=submenu_id
        )
        return item

    async def get_all_dishes(
        self, menu_id: str, submenu_id: str, background_task: BackgroundTasks
    ) -> list[Dish]:
        cache = await self.cacher.get_all_dishes(menu_id=menu_id, submenu_id=submenu_id)
        if cache:
            return cache
        item = await self.crud.get_all_dishes_data(submenu_id=submenu_id)
        background_task.add_task(
            self.cacher.set_all_dishes,
            menu_id=menu_id,
            submenu_id=submenu_id,
            item=item,
        )
        return item

    async def update_dish(
        self,
        menu_id: str,
        submenu_id: str,
        dish_id: str,
        data: DishCreate,
        background_task: BackgroundTasks,
    ) -> Dish | dict:
        item = await self.crud.update_dish_data(dish_id=dish_id, data=data)
        background_task.add_task(
            self.cacher.delete_dish_by_id,
            menu_id=menu_id,
            submenu_id=submenu_id,
            dish_id=dish_id,
        )
        background_task.add_task(self.cacher.delete_all_menu)
        background_task.add_task(self.cacher.delete_all_submenus, menu_id=menu_id)
        background_task.add_task(
            self.cacher.delete_all_dishes, menu_id=menu_id, submenu_id=submenu_id
        )
        background_task.add_task(self.cacher.delete_menu_and_submenu_and_dishes)
        return item

    async def delete_dish(
        self,
        menu_id: str,
        submenu_id: str,
        dish_id: str,
        background_task: BackgroundTasks,
    ) -> dict:
        await self.cacher.delete_dish_by_id(
            menu_id=menu_id, submenu_id=submenu_id, dish_id=dish_id
        )
        item = await self.crud.delete_dish_data(dish_id=dish_id)
        background_task.add_task(self.cacher.delete_all_menu)
        background_task.add_task(self.cacher.delete_all_submenus, menu_id=menu_id)
        background_task.add_task(
            self.cacher.delete_all_dishes, menu_id=menu_id, submenu_id=submenu_id
        )
        background_task.add_task(self.cacher.delete_menu_and_submenu_and_dishes)
        background_task.add_task(self.cacher.delete_menu_cache, menu_id=menu_id)
        background_task.add_task(
            self.cacher.delete_submenu_by_id, menu_id=menu_id, submenu_id=submenu_id
        )
        return item
