from tests.conftest import client
from tests.test_menu_crud import (
    create_menu,
    delete_menu,
    check_empty_menu_list,
)
from tests.test_submenu_crud import (
    create_submenu,
    delete_submenu,
    check_empty_submenu_list,
)


def create_dish(
    submenu_id: str, menu_id: str, title: str, description: str, price: str
):
    response = client.post(
        f"/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes",
        json={
            "menu_id": menu_id,
            "submenu_id": submenu_id,
            "title": title,
            "description": description,
            "price": price,
        },
    )
    return response


def check_all_dish(submenu_id: str, menu_id: str):
    response = client.get(f"/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes")
    return response


def check_dish(dish_id: str, submenu_id: str, menu_id: str):
    response = client.get(
        f"/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}"
    )
    return response


def update_dish(
    dish_id: str,
    submenu_id: str,
    menu_id: str,
    title: str,
    description: str,
    price: str,
):
    response = client.patch(
        f"/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}",
        json={
            "title": title,
            "description": description,
            "price": price,
        },
    )
    return response


def delete_dish(dish_id: str, submenu_id: str, menu_id: str):
    response = client.delete(
        f"/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}"
    )
    return response


def check_dish_empty_list(menu_id: str, submenu_id: str):
    response = check_all_dish(menu_id=menu_id, submenu_id=submenu_id)
    assert response.status_code == 200, response.text
    assert response.json() == []


def check_dish_not_empty_list(menu_id: str, submenu_id: str):
    response = check_all_dish(menu_id=menu_id, submenu_id=submenu_id)
    assert response.status_code == 200, response.text
    assert response.json() != []


def test_dish():
    # Create menu
    menu_create = create_menu()
    assert menu_create.status_code == 201, menu_create.text
    menu_data = menu_create.json()
    assert "id" in menu_data
    menu_id = menu_data["id"]

    # Create submenu
    submenu_create = create_submenu(
        menu_id=menu_id, title="My submenu 1", description="My submenu description 1"
    )
    assert submenu_create.status_code == 201, submenu_create.text
    sub_data = submenu_create.json()
    assert "id" in sub_data
    submenu_id = sub_data["id"]

    # check empty list of dish
    check_dish_empty_list(menu_id=menu_id, submenu_id=submenu_id)

    # Create dish
    dish_create = create_dish(
        menu_id=menu_id,
        submenu_id=submenu_id,
        title="My dish 1",
        description="My dish description 1",
        price="12.50",
    )
    assert dish_create.status_code == 201, dish_create.text
    dish_data = dish_create.json()
    assert all(
        map(lambda item: item in dish_data, ("id", "title", "description", "price"))
    )
    dish_id = dish_data["id"]

    # Check dish list (not empty)
    check_dish_not_empty_list(menu_id=menu_id, submenu_id=submenu_id)

    # Check dish
    dish_check = check_dish(menu_id=menu_id, submenu_id=submenu_id, dish_id=dish_id)
    assert dish_check.status_code == 200, dish_check.text
    assert all(
        map(
            lambda item: item in dish_check.json(),
            ("id", "title", "description", "price"),
        )
    )

    # update dish
    dish_update = update_dish(
        menu_id=menu_id,
        submenu_id=submenu_id,
        dish_id=dish_id,
        title="My updated dish 1",
        description="My updated dish description 1",
        price="14.50",
    )
    assert dish_update.status_code == 200, dish_update.text
    update_dish_data = dish_update.json()
    assert all(
        map(
            lambda item: item in update_dish_data,
            ("id", "title", "description", "price"),
        )
    )
    assert (
        dish_data["title"] != update_dish_data["title"]
        and dish_data["description"] != update_dish_data["description"]
        and dish_data["price"] != update_dish_data["price"]
    )

    # CHeck dish update data
    check_dish_update_data = check_dish(
        menu_id=menu_id, submenu_id=submenu_id, dish_id=dish_id
    )
    assert check_dish_update_data.status_code == 200, check_dish_update_data.text
    updated_dish_data = check_dish_update_data.json()
    assert updated_dish_data == update_dish_data

    # Delete dish
    dish_delete = delete_dish(menu_id=menu_id, submenu_id=submenu_id, dish_id=dish_id)
    assert dish_delete.status_code == 200, dish_delete.text

    # Check empty dish list
    check_dish_empty_list(menu_id=menu_id, submenu_id=submenu_id)

    # Check dish
    check_deleted_dish = check_dish(
        menu_id=menu_id, submenu_id=submenu_id, dish_id=dish_id
    )
    assert check_deleted_dish.status_code == 404, check_deleted_dish.text
    assert check_deleted_dish.json() == {"detail": "dish not found"}

    # delete submenu
    delete_submenu_response = delete_submenu(menu_id=menu_id, submenu_id=submenu_id)
    assert delete_submenu_response.status_code == 200, delete_submenu_response.text

    # Check submenu list is empty
    check_empty_submenu_list(menu_id=menu_id)

    # delete menu
    delete_menu_response = delete_menu(menu_id=menu_id)
    assert delete_menu_response.status_code == 200, delete_menu_response.text

    # Check menu empty list
    check_empty_menu_list()
