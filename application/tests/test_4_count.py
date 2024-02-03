from fastapi.testclient import TestClient

from .test_1_menu_crud import create_menu_by_id, delete_menu, get_menu, json_create_menu
from .test_2_submenu_crud import (
    create_submenu_by_id,
    delete_submenu,
    get_all_submenu,
    get_submenu,
    json_submenu_create,
)
from .test_3_dishes_crud import create_dish_by_id, get_all_dish, json_dishes_create


def test_count(client: TestClient, get_all_menus):
    # Create menu
    create_menu_response = create_menu_by_id(client=client)
    assert create_menu_response.status_code == 201, create_menu_response.text
    menu_data = create_menu_response.json()
    assert all(map(lambda item: item in menu_data, ('id', 'title', 'description')))
    assert menu_data['title'] == json_create_menu['title']
    assert menu_data['description'] == json_create_menu['description']
    menu_id = menu_data['id']

    # Create submenu
    create_submenu_response = create_submenu_by_id(client=client, menu_id=menu_id)
    assert create_submenu_response.status_code == 201, create_submenu_response.text
    submenu_data = create_submenu_response.json()
    assert all(map(lambda item: item in submenu_data, ('id', 'title', 'description')))
    assert submenu_data['title'] == json_submenu_create['title']
    assert submenu_data['description'] == json_submenu_create['description']
    submenu_id = submenu_data['id']

    # Create dish_1
    json_dish_1 = {
        'title': 'My dish 2',
        'description': 'My dish description 2',
        'price': '13.50',
    }
    create_dish_1_response = create_dish_by_id(
        client=client,
        menu_id=menu_id,
        submenu_id=submenu_id,
        title=json_dish_1['title'],
        description=json_dish_1['description'],
        price=json_dish_1['price'],
    )
    assert create_dish_1_response.status_code == 201, create_dish_1_response.text
    dish_1_data = create_dish_1_response.json()
    assert all(
        map(lambda item: item in dish_1_data, ('id', 'title', 'description', 'price'))
    )
    assert dish_1_data['title'] == json_dish_1['title']
    assert dish_1_data['description'] == json_dish_1['description']
    assert dish_1_data['price'] == json_dish_1['price']

    # Create dish_2
    create_dish_2_response = create_dish_by_id(
        client=client, menu_id=menu_id, submenu_id=submenu_id
    )
    assert create_dish_2_response.status_code == 201, create_dish_2_response.text
    dish_2_data = create_dish_2_response.json()
    assert all(
        map(lambda item: item in dish_2_data, ('id', 'title', 'description', 'price'))
    )
    assert dish_2_data['title'] == json_dishes_create['title']
    assert dish_2_data['description'] == json_dishes_create['description']
    assert dish_2_data['price'] == json_dishes_create['price']

    # Check menu
    check_menu_response = get_menu(client=client, menu_id=menu_id)
    assert check_menu_response.status_code == 200, check_menu_response.text
    check_menu_data = check_menu_response.json()
    assert all(
        map(lambda item: item in check_menu_data, ('id', 'title', 'description'))
    )
    assert check_menu_data['id'] == menu_id
    assert check_menu_data['dishes_count'] == 2
    assert check_menu_data['submenus_count'] == 1

    # Check submenu
    check_submenu_response = get_submenu(
        client=client, menu_id=menu_id, submenu_id=submenu_id
    )
    assert check_submenu_response.status_code == 200, check_submenu_response.text
    check_submenu_data = check_submenu_response.json()
    assert all(
        map(lambda item: item in check_submenu_data, ('id', 'title', 'description'))
    )
    assert check_submenu_data['id'] == submenu_id
    assert check_submenu_data['dishes_count'] == 2

    # Delete submenu
    delete_submenu_response = delete_submenu(
        client=client, menu_id=menu_id, submenu_id=submenu_id
    )
    assert delete_submenu_response.status_code == 200, delete_submenu_response.text

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

    # Check menu
    check_menu_1_response = get_menu(client=client, menu_id=menu_id)
    assert check_menu_1_response.status_code == 200, check_menu_1_response.text
    check_1_menu_data = check_menu_1_response.json()
    assert all(
        map(lambda item: item in check_1_menu_data, ('id', 'title', 'description'))
    )
    assert check_1_menu_data['dishes_count'] == 0
    assert check_1_menu_data['submenus_count'] == 0

    # Delete menu
    delete_menu_1_response = delete_menu(client=client, menu_id=menu_id)
    assert delete_menu_1_response.status_code == 200, delete_menu_1_response.text

    # Check list of menu
    check_list_menu = get_all_menus
    assert check_list_menu.status_code == 200, check_list_menu.text
    assert check_list_menu.json() == []
