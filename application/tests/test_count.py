from .test_menu_crud import (
    create_menu,
    delete_menu,
    check_empty_menu_list,
    check_menu,
)
from .test_submenu_crud import (
    create_submenu,
    delete_submenu,
    check_empty_submenu_list,
    check_submenu,
)
from .test_dishes_crud import (
    create_dish,
    check_dish_empty_list,
)


def test_count():
    # Create menu
    create_menu_response = create_menu()
    assert create_menu_response.status_code == 201, create_menu_response.text
    menu_data = create_menu_response.json()
    assert "id" in menu_data
    menu_id = menu_data["id"]

    # Create submenu
    create_submenu_response = create_submenu(
        menu_id=menu_id, title="My submenu 1", description="My submenu description 1"
    )
    assert create_submenu_response.status_code == 201, create_submenu_response.text
    submenu_data = create_submenu_response.json()
    assert "id" in submenu_data
    submenu_id = submenu_data["id"]

    # Create dish 1
    create_dish_1_response = create_dish(
        menu_id=menu_id,
        submenu_id=submenu_id,
        title="My dish 2",
        description="My dish description 2",
        price="13.50",
    )
    assert create_dish_1_response.status_code == 201, create_dish_1_response.text
    dish_1_data = create_dish_1_response.json()
    assert "id" in dish_1_data
    dish_id_1 = dish_1_data["id"]

    # Create dish 2
    create_dish_2_response = create_dish(
        menu_id=menu_id,
        submenu_id=submenu_id,
        title="My dish 1",
        description="My dish description 1",
        price="12.50",
    )
    assert create_dish_2_response.status_code == 201, create_dish_2_response.text
    dish_2_data = create_dish_2_response.json()
    assert "id" in dish_2_data
    dish_id_2 = dish_2_data["id"]

    # Check menu
    check_menu_response = check_menu(menu_id=menu_id)
    assert check_menu_response.status_code == 200, check_menu_response.text
    checking_menu_data = check_menu_response.json()
    assert "id" in checking_menu_data
    assert checking_menu_data["id"] == menu_id
    assert (
        checking_menu_data["submenus_count"] == 1
        and checking_menu_data["dishes_count"] == 2
    )

    # Check submenu
    checking_submenu_response = check_submenu(menu_id=menu_id, submenu_id=submenu_id)
    assert checking_submenu_response.status_code == 200, create_submenu_response.text
    checking_submenu_data = checking_submenu_response.json()
    assert "id" in checking_submenu_data
    assert checking_submenu_data["id"] == submenu_id
    assert checking_submenu_data["dishes_count"] == 2

    # Delete submenu
    delete_submenu_response = delete_submenu(menu_id=menu_id, submenu_id=submenu_id)
    assert delete_submenu_response.status_code == 200, delete_submenu_response.text

    # Check empty submenu list
    check_empty_submenu_list(menu_id=menu_id)

    # Check empty dishes list
    check_dish_empty_list(menu_id=menu_id, submenu_id=submenu_id)

    # Check menu
    new_check_menu_response = check_menu(menu_id=menu_id)
    assert new_check_menu_response.status_code == 200, new_check_menu_response.text
    checking_new_menu_data = new_check_menu_response.json()
    assert "id" in checking_new_menu_data
    assert checking_new_menu_data["id"] == menu_id
    assert (
        checking_new_menu_data["submenus_count"] == 0
        and checking_new_menu_data["dishes_count"] == 0
    )

    # delete menu
    delete_menu_response = delete_menu(menu_id=menu_id)
    assert delete_menu_response.status_code == 200, delete_menu_response.text

    # Check empty menu list
    check_empty_menu_list()
