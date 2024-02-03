from core.cache_repository import CacheRepository
from dishes.crud_repository import DishesRepository
from dishes.schemas import DishCreate, DishResponse
from fastapi import Depends


class DishesService:
    def __init__(
        self, cacher: CacheRepository = Depends(), crud: DishesRepository = Depends()
    ) -> None:
        self.cacher = cacher
        self.crud = crud

    def get_dish(self, menu_id: str, submenu_id: str, dish_id: str) -> DishResponse:
        cache = self.cacher.get_dish_by_id(
            menu_id=menu_id, submenu_id=submenu_id, dish_id=dish_id
        )
        if cache:
            return cache
        item = self.crud.get_dish_data(submenu_id=submenu_id, dish_id=dish_id)
        self.cacher.set_dish(
            menu_id=menu_id, submenu_id=submenu_id, dish_id=dish_id, data=item
        )
        return item

    def create_dish(
        self, menu_id: str, submenu_id: str, data: DishCreate
    ) -> DishResponse:
        item = self.crud.create_dish(submenu_id=submenu_id, data=data)
        dish_id = item.id
        self.cacher.set_dish(
            menu_id=menu_id, submenu_id=submenu_id, dish_id=dish_id, data=item
        )
        self.update_all_dishes(menu_id=menu_id, submenu_id=submenu_id)
        return item

    def get_all_dishes(
        self,
        menu_id: str,
        submenu_id: str,
    ) -> list[DishResponse]:
        cache = self.cacher.get_all_dishes(menu_id=menu_id, submenu_id=submenu_id)
        if cache:
            # item = pickle.loads(cache)
            return cache
        item = self.crud.get_all_dishes_data(submenu_id=submenu_id)
        self.cacher.set_all_dishes(menu_id=menu_id, submenu_id=submenu_id, item=item)
        return item

    def update_dish(
        self, menu_id: str, submenu_id: str, dish_id: str, data: DishCreate
    ) -> DishResponse | dict:
        item = self.crud.update_dish_data(dish_id=dish_id, data=data)
        self.cacher.update_dish_by_id(
            menu_id=menu_id, submenu_id=submenu_id, dish_id=dish_id, item=item
        )
        self.update_all_dishes(menu_id=menu_id, submenu_id=submenu_id)
        return item

    def delete_dish(self, menu_id: str, submenu_id: str, dish_id: str) -> dict:
        self.cacher.delete_dish_by_id(
            menu_id=menu_id, submenu_id=submenu_id, dish_id=dish_id
        )
        item = self.crud.delete_dish_data(dish_id=dish_id)
        self.update_all_dishes(menu_id=menu_id, submenu_id=submenu_id)
        return item

    def update_all_dishes(self, menu_id: str, submenu_id: str) -> None:
        self.cacher.delete_all_dishes(menu_id=menu_id, submenu_id=submenu_id)
        item = self.crud.get_all_dishes_data(submenu_id=submenu_id)
        self.cacher.set_all_dishes(menu_id=menu_id, submenu_id=submenu_id, item=item)
