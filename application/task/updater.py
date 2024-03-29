import requests

from core.config import (
    MENUS_URL,
    MENU_URL,
    SUBMENU_URL,
    SUBMENUS_URL,
    DISH_URL,
    DISHES_URL,
    LINK,
)


class UpdateBase:
    def __init__(self, parser_data: list[dict]) -> None:
        self.data = parser_data

    def get_list_of_menus_id(self) -> list[str]:
        r = requests.get(url=LINK + MENUS_URL)
        if r.json():
            list_of_menus = [item["id"] for item in r.json()]
            return list_of_menus
        return []

    def get_list_of_submenus_id(self, menu_id: str) -> list[str]:
        r = requests.get(url=LINK + SUBMENUS_URL.format(menu_id=menu_id))
        if r.json():
            list_of_submenus = [item["id"] for item in r.json()]
            return list_of_submenus
        return []

    def get_list_of_dishes_id(self, menu_id: str, submenu_id: str) -> list[str]:
        r = requests.get(
            url=LINK + DISHES_URL.format(menu_id=menu_id, submenu_id=submenu_id)
        )
        if r.json():
            list_of_dishes = [item["id"] for item in r.json()]
            return list_of_dishes
        return []

    def delete_menu(self, menu_id: str) -> None:
        delete_request = requests.delete(url=LINK + MENU_URL.format(menu_id=menu_id))

    def delete_submenu(self, menu_id: str, submenu_id: str) -> None:
        delete_request = requests.delete(
            url=LINK + SUBMENU_URL.format(menu_id=menu_id, submenu_id=submenu_id)
        )

    def delete_dish(self, menu_id: str, submenu_id: str, dish_id: str) -> None:
        delete_request = requests.delete(
            url=LINK
            + DISH_URL.format(menu_id=menu_id, submenu_id=submenu_id, dish_id=dish_id)
        )

    def update_menu(self, menu_id: str, update_data: dict) -> None:
        data = {
            "title": update_data["title"],
            "description": update_data["description"],
        }
        update_request = requests.patch(
            url=LINK + MENU_URL.format(menu_id=menu_id), json=data
        )

    def update_submenu(self, menu_id: str, submenu_id: str, update_data: dict) -> None:
        data = {
            "title": update_data["title"],
            "description": update_data["description"],
        }
        update_request = requests.patch(
            url=LINK + SUBMENU_URL.format(menu_id=menu_id, submenu_id=submenu_id),
            json=data,
        )

    def update_dish(
        self, menu_id: str, submenu_id: str, dish_id: str, update_data: dict
    ) -> None:
        discount = update_data.get("discount", 0)
        data = {
            "title": update_data["title"],
            "description": update_data["description"],
            "price": str(update_data["price"]),
            "discount": discount,
        }
        update_request = requests.patch(
            url=LINK
            + DISH_URL.format(menu_id=menu_id, submenu_id=submenu_id, dish_id=dish_id),
            json=data,
        )

    def create_menu(self, data_in: dict) -> None:
        data = {
            "id": data_in["id"],
            "title": data_in["title"],
            "description": data_in["description"],
        }
        create_response = requests.post(url=LINK + MENUS_URL, json=data)

    def create_submenu(self, menu_id: str, data_in: dict) -> None:
        data = {
            "id": data_in["id"],
            "title": data_in["title"],
            "description": data_in["description"],
        }
        create_response = requests.post(
            url=LINK + SUBMENUS_URL.format(menu_id=menu_id), json=data
        )

    def create_dish(self, menu_id: str, submenu_id: str, data_in: dict) -> None:
        discount = data_in.get("discount", 0)
        data = {
            "id": data_in["id"],
            "title": data_in["title"],
            "description": data_in["description"],
            "price": str(data_in["price"]),
            "discount": discount,
        }
        create_response = requests.post(
            url=LINK + DISHES_URL.format(menu_id=menu_id, submenu_id=submenu_id),
            json=data,
        )

    def start_update(self) -> None:
        list_of_menus = self.get_list_of_menus_id()
        if list_of_menus:
            list_of_corrent_menu = [item["id"] for item in self.data]
            for m_id in list_of_menus:
                if m_id not in list_of_corrent_menu:
                    self.delete_menu(menu_id=m_id)

        for menus in self.data:
            menu_id = menus["id"]
            if menu_id not in list_of_menus:
                self.create_menu(data_in=menus)
            else:
                self.update_menu(menu_id=menu_id, update_data=menus)

            submenus_list = self.get_list_of_submenus_id(menu_id=menu_id)

            if submenus_list:
                list_of_corrent_submenu = [item["id"] for item in menus["submenus"]]
                for s_id in submenus_list:
                    if s_id not in list_of_corrent_submenu:
                        self.delete_submenu(menu_id=menu_id, submenu_id=s_id)

            for submenus in menus["submenus"]:
                submenu_id = submenus["id"]
                if submenu_id not in submenus_list:
                    self.create_submenu(menu_id=menu_id, data_in=submenus)
                else:
                    self.update_submenu(
                        menu_id=menu_id, submenu_id=submenu_id, update_data=submenus
                    )

                dishes_list = self.get_list_of_dishes_id(
                    menu_id=menu_id, submenu_id=submenu_id
                )
                if dishes_list:
                    list_of_corrent_dishes = [item["id"] for item in submenus["dishes"]]
                    for d_id in dishes_list:
                        if d_id not in list_of_corrent_dishes:
                            self.delete_dish(
                                menu_id=menu_id, submenu_id=submenu_id, dish_id=d_id
                            )

                for dish in submenus["dishes"]:
                    dish_id = dish["id"]
                    if dish_id not in dishes_list:
                        self.create_dish(
                            menu_id=menu_id, submenu_id=submenu_id, data_in=dish
                        )
                    else:
                        self.update_dish(
                            menu_id=menu_id,
                            submenu_id=submenu_id,
                            dish_id=dish_id,
                            update_data=dish,
                        )
