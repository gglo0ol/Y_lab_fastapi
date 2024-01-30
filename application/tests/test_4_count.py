from fastapi.testclient import TestClient

from .test_1_menu_crud import create_menu, delete_menu, get_menu
from .test_3_dishes_crud import create_dish, delete_dish, get_all_dish
from .test_2_submenu_crud import (
    create_submenu,
    delete_submenu,
    get_submenu,
    get_all_submenu,
)


def test_count(client: TestClient):
    # Create menu
    create_menu_response = create_menu(client=client)
    assert create_menu_response.status_code == 201, create_menu_response.text
    menu_data = create_menu_response.json()
    assert all(map(lambda item: item in menu_data, ("id", "title", "description")))
    menu_id = menu_data["id"]

    # Create submenu
    create_submenu_response = create_submenu(client=client, menu_id=menu_id)
    assert create_submenu_response.status_code == 201, create_submenu_response.text
    submenu_data = create_submenu_response.json()
    assert all(map(lambda item: item in submenu_data, ("id", "title", "description")))
    submenu_id = submenu_data["id"]

    # Create dish_1
    create_dish_1_response = create_dish(
        client=client,
        menu_id=menu_id,
        submenu_id=submenu_id,
        title="My dish 2",
        description="My dish description 2",
        price="13.50",
    )
    assert create_dish_1_response.status_code == 201, create_dish_1_response.text
    dish_1_data = create_dish_1_response.json()
    assert all(
        map(lambda item: item in dish_1_data, ("id", "title", "description", "price"))
    )
    dish_1_id = dish_1_data["id"]

    # Create dish_2
    create_dish_2_response = create_dish(
        client=client, menu_id=menu_id, submenu_id=submenu_id
    )
    assert create_dish_2_response.status_code == 201, create_dish_2_response.text
    dish_2_data = create_dish_2_response.json()
    assert all(
        map(lambda item: item in dish_2_data, ("id", "title", "description", "price"))
    )
    dish_2_id = dish_2_data["id"]

    # Check menu
    check_menu_response = get_menu(client=client, menu_id=menu_id)
    assert check_menu_response.status_code == 200, check_menu_response.text
    check_menu_data = check_menu_response.json()
    assert all(
        map(lambda item: item in check_menu_data, ("id", "title", "description"))
    )
    assert check_menu_data["id"] == menu_id
    assert check_menu_data["dishes_count"] == 2
    assert check_menu_data["submenus_count"] == 1

    # Check submenu
    check_submenu_response = get_submenu(
        client=client, menu_id=menu_id, submenu_id=submenu_id
    )
    assert check_submenu_response.status_code == 200, check_submenu_response.text
    check_submenu_data = check_submenu_response.json()
    assert all(
        map(lambda item: item in check_submenu_data, ("id", "title", "description"))
    )
    assert check_submenu_data["id"] == submenu_id
    assert check_submenu_data["dishes_count"] == 2

    # Delete submenu
    delete_submenu_response = delete_submenu(
        client=client, menu_id=menu_id, submenu_id=submenu_id
    )
    assert delete_submenu_response.status_code == 200, delete_submenu_response.text
    print(delete_submenu_response.json())

    # Check menu
    check_deleted_submenu_response = get_all_submenu(client=client, menu_id=menu_id)
    assert (
        check_deleted_submenu_response.status_code == 200
    ), check_deleted_submenu_response.text
    assert check_deleted_submenu_response.json() == []

    # Check submenu
    submenu_response = get_all_dish(
        client=client, menu_id=menu_id, submenu_id=submenu_id
    )
    assert submenu_response.status_code == 200, submenu_response.text
    assert submenu_response.json() == []


#
#     # Create submenu
#     create_submenu_response = create_submenu(
#         menu_id=menu_id, title="My submenu 1", description="My submenu description 1"
#     )
#     assert create_submenu_response.status_code == 201, create_submenu_response.text
#     submenu_data = create_submenu_response.json()
#     assert "id" in submenu_data
#     submenu_id = submenu_data["id"]
#
#     # Create dish 1
#     create_dish_1_response = create_dish(
#         menu_id=menu_id,
#         submenu_id=submenu_id,
#         title="My dish 2",
#         description="My dish description 2",
#         price="13.50",
#     )
#     assert create_dish_1_response.status_code == 201, create_dish_1_response.text
#     dish_1_data = create_dish_1_response.json()
#     assert "id" in dish_1_data
#     dish_id_1 = dish_1_data["id"]
#
#     # Create dish 2
#     create_dish_2_response = create_dish(
#         menu_id=menu_id,
#         submenu_id=submenu_id,
#         title="My dish 1",
#         description="My dish description 1",
#         price="12.50",
#     )
#     assert create_dish_2_response.status_code == 201, create_dish_2_response.text
#     dish_2_data = create_dish_2_response.json()
#     assert "id" in dish_2_data
#     dish_id_2 = dish_2_data["id"]
#
#     # Check menu
#     check_menu_response = check_menu(menu_id=menu_id)
#     assert check_menu_response.status_code == 200, check_menu_response.text
#     checking_menu_data = check_menu_response.json()
#     assert "id" in checking_menu_data
#     assert checking_menu_data["id"] == menu_id
#     assert (
#         checking_menu_data["submenus_count"] == 1
#         and checking_menu_data["dishes_count"] == 2
#     )
#
#     # Check submenu
#     checking_submenu_response = check_submenu(menu_id=menu_id, submenu_id=submenu_id)
#     assert checking_submenu_response.status_code == 200, create_submenu_response.text
#     checking_submenu_data = checking_submenu_response.json()
#     assert "id" in checking_submenu_data
#     assert checking_submenu_data["id"] == submenu_id
#     assert checking_submenu_data["dishes_count"] == 2
#
#     # Delete submenu
#     delete_submenu_response = delete_submenu(menu_id=menu_id, submenu_id=submenu_id)
#     assert delete_submenu_response.status_code == 200, delete_submenu_response.text
#
#     # Check empty submenu list
#     check_empty_submenu_list(menu_id=menu_id)
#
#     # Check empty dishes list
#     check_dish_empty_list(menu_id=menu_id, submenu_id=submenu_id)
#
#     # Check menu
#     new_check_menu_response = check_menu(menu_id=menu_id)
#     assert new_check_menu_response.status_code == 200, new_check_menu_response.text
#     checking_new_menu_data = new_check_menu_response.json()
#     assert "id" in checking_new_menu_data
#     assert checking_new_menu_data["id"] == menu_id
#     assert (
#         checking_new_menu_data["submenus_count"] == 0
#         and checking_new_menu_data["dishes_count"] == 0
#     )
#
#     # delete menu
#     delete_menu_response = delete_menu(menu_id=menu_id)
#     assert delete_menu_response.status_code == 200, delete_menu_response.text
#
#     # Check empty menu list
#     check_empty_menu_list()
