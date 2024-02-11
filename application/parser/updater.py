import requests

from core.config import (
    MENUS_URL,
    MENU_URL,
    SUBMENU_URL,
    SUBMENUS_URL,
    DISH_URL,
    DISHES_URL,
)
from menus.schemas import MenuCreate
from submenus.schemas import SubmenuCreate
from dishes.schemas import DishCreate

# from menus.service_repository import MenuService
# from submenus.servise_repository import SubmenuService
# from dishes.service_repository import DishesService


class UpdateBase:
    def __init__(self, parser_data: list[dict]) -> None:
        self.data = parser_data

    def get_list_of_menus_id(self) -> list[str]:
        r = requests.get(url=MENUS_URL)
        list_of_menus = [item.id for item in r.json()]
        return list_of_menus

    def get_list_of_submenus_id(self, menu_id: str) -> list[str]:
        r = requests.get(url=SUBMENUS_URL.format(menu_id=menu_id))
        list_of_menus = [item.id for item in r.json()]
        return list_of_menus

    def get_list_of_dishes_id(self, menu_id: str, submenu_id: str) -> list[str]:
        r = requests.get(url=DISHES_URL.format(menu_id=menu_id, submenu_id=submenu_id))
        list_of_menus = [item.id for item in r.json()]
        return list_of_menus

    def delete_menu(self, menu_id: str) -> None:
        delete_request = requests.delete(url=MENU_URL.format(menu_id=menu_id))

    def delete_submenu(self, menu_id: str, submenu_id: str) -> None:
        delete_request = requests.delete(
            url=MENU_URL.format(menu_id=menu_id, submenu_id=submenu_id)
        )

    def delete_dish(self, menu_id: str, submenu_id: str, dish_id: str) -> None:
        delete_request = requests.delete(
            url=DISH_URL.format(menu_id=menu_id, submenu_id=submenu_id, dish_id=dish_id)
        )

    def update_menu(self, menu_id: str, update_data: dict) -> None:
        data = {
            "title": update_data["title"],
            "description": update_data["description"],
        }
        update_request = requests.patch(url=MENU_URL.format(menu_id=menu_id), json=data)

    def update_submenu(self, menu_id: str, submenu_id: str, update_data: dict) -> None:
        data = {
            "title": update_data["title"],
            "description": update_data["description"],
        }
        update_request = requests.patch(
            url=SUBMENU_URL.format(menu_id=menu_id, submenu_id=submenu_id), json=data
        )

    def update_dish(
        self, menu_id: str, submenu_id: str, dish_id: str, update_data: dict
    ) -> None:
        data = {
            "title": update_data["title"],
            "description": update_data["description"],
            "price": update_data["price"],
            "discount": update_data["discount"],
        }
        update_request = requests.patch(
            url=SUBMENU_URL.format(
                menu_id=menu_id, submenu_id=submenu_id, dish_id=dish_id
            ),
            json=data,
        )

    # def crete_menu(self, data_in: MenuCreate) -> None:
    #     data = {
    #         "title": data_in.title,
    #         "description": data_in.description,
    #     }
    #     update_request = requests.post(url=MENUS_URL, json=data)
    #
    # def create_submenu(self, menu_id: str, data_in: SubmenuCreate) -> None:
    #     data = {
    #         "title": data_in.title,
    #         "description": data_in.description,
    #     }
    #     update_request = requests.post(
    #         url=SUBMENUS_URL.format(menu_id=menu_id), json=data
    #     )
    #
    # def create_dish(self, menu_id: str, submenu_id: str, data_in: DishCreate) -> None:
    #     data = {
    #         "title": data_in.title,
    #         "description": data_in.description,
    #         "price": data_in.price,
    #         "discount": data_in.discount,
    #     }
    #     update_request = requests.post(
    #         url=SUBMENUS_URL.format(menu_id=menu_id, submenu_id=submenu_id), json=data
    #     )

    def check_menu_data(self, menu_id: str):
        menu_from_data = self.data

    def start_update(self):
        for id in self.get_list_of_menus_id():
            if id not in list(map(lambda item: item["id"], self.data)):
                self.delete_menu(menu_id=id)

        for menus in self.data:
            menu_id = menus["id"]
            self.update_menu(menu_id=menu_id, update_data=menus)
            for id in self.get_list_of_submenus_id(menu_id=menu_id):
                if id not in list(map(lambda item: item["id"], menus["submenus"])):
                    self.delete_submenu(menu_id=menu_id, submenu_id=id)

            for submenus in menus["submenus"]:
                submenu_id = submenus["id"]
                self.update_submenu(
                    menu_id=menu_id, submenu_id=submenu_id, update_data=submenus
                )

                for id in self.get_list_of_dishes_id(
                    menu_id=menu_id, submenu_id=submenu_id
                ):
                    if id not in submenus["dishes"]:
                        self.delete_dish(
                            menu_id=menu_id, submenu_id=submenu_id, dish_id=id
                        )

                for dish in submenus["dishes"]:
                    dish_id = dish["id"]
                    self.update_dish(
                        menu_id=menu_id,
                        submenu_id=submenu_id,
                        dish_id=dish_id,
                        update_data=dish,
                    )
