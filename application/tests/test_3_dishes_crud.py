from dishes.views import (
    create_dish_endpoint,
    delete_dish_endpoint,
    get_all_dishes_endpoint,
    get_dish_endpoint,
    update_dish_endpoint,
)
from fastapi.testclient import TestClient
from menus.views import create_menu_endpoint, delete_menu_endpoint
from submenus.views import create_submenu_endpoint
from tests.conftest import reverse


def test_get_empty_dishes_list(
    client: TestClient, saved_data: dict, data_menu_create, data_submenu_create
) -> None:
    create_menu_response = client.post(
        reverse(create_menu_endpoint), json=data_menu_create
    )
    saved_data['menu'] = create_menu_response.json()
    menu_id = saved_data['menu']['id']
    create_submenu_response = client.post(
        reverse(create_submenu_endpoint, menu_id=menu_id), json=data_submenu_create
    )
    saved_data['submenu'] = create_submenu_response.json()
    submenu_id = saved_data['submenu']['id']
    all_dishes_list_response = client.get(
        reverse(get_all_dishes_endpoint, menu_id=menu_id, submenu_id=submenu_id)
    )
    assert all_dishes_list_response.status_code == 200, all_dishes_list_response.text
    assert all_dishes_list_response.json() == []


def test_create_dish(
    client: TestClient, saved_data: dict, data_dishes_create: dict
) -> None:
    menu_id = saved_data['menu']['id']
    submenu_id = saved_data['submenu']['id']
    dish_create_response = client.post(
        reverse(create_dish_endpoint, menu_id=menu_id, submenu_id=submenu_id),
        json=data_dishes_create,
    )
    assert dish_create_response.status_code == 201, dish_create_response.text
    dish_data = dish_create_response.json()
    assert all(
        map(lambda item: item in dish_data, ('id', 'title', 'description', 'price'))
    )
    assert dish_data['title'] == data_dishes_create['title']
    assert dish_data['description'] == data_dishes_create['description']
    assert dish_data['price'] == data_dishes_create['price']
    saved_data['dish'] = dish_data


def test_not_empty_dishes_list(client: TestClient, saved_data: dict) -> None:
    menu_id = saved_data['menu']['id']
    submenu_id = saved_data['submenu']['id']
    check_not_empty_dishes_list = client.get(
        reverse(get_all_dishes_endpoint, menu_id=menu_id, submenu_id=submenu_id)
    )
    assert (
        check_not_empty_dishes_list.status_code == 200
    ), check_not_empty_dishes_list.text
    assert check_not_empty_dishes_list.json() != []


def test_get_dish(client: TestClient, saved_data: dict) -> None:
    menu_id = saved_data['menu']['id']
    submenu_id = saved_data['submenu']['id']
    dish_id = saved_data['dish']['id']
    get_dish_response = client.get(
        reverse(
            get_dish_endpoint, menu_id=menu_id, submenu_id=submenu_id, dish_id=dish_id
        )
    )
    assert get_dish_response.status_code == 200, get_dish_response.text
    dish_data = get_dish_response.json()
    assert all(
        map(
            lambda item: item in dish_data,
            ('id', 'title', 'description', 'price'),
        )
    )
    assert dish_data['title'] == saved_data['dish']['title']
    assert dish_data['description'] == saved_data['dish']['description']
    assert dish_data['price'] == saved_data['dish']['price']


def test_update_dish(
    client: TestClient, saved_data: dict, data_dishes_update: dict
) -> None:
    menu_id = saved_data['menu']['id']
    submenu_id = saved_data['submenu']['id']
    dish_id = saved_data['dish']['id']

    update_dish_response = client.patch(
        reverse(
            update_dish_endpoint,
            menu_id=menu_id,
            submenu_id=submenu_id,
            dish_id=dish_id,
        ),
        json=data_dishes_update,
    )
    assert update_dish_response.status_code == 200, update_dish_response.text

    check_updated_dish = client.get(
        reverse(
            get_dish_endpoint, menu_id=menu_id, submenu_id=submenu_id, dish_id=dish_id
        )
    )
    assert check_updated_dish.status_code == 200, check_updated_dish.text
    check_updated_dish_data = check_updated_dish.json()
    assert all(
        map(
            lambda item: item in check_updated_dish_data,
            ('id', 'title', 'description', 'price'),
        )
    )
    assert check_updated_dish_data['title'] == data_dishes_update['title']
    assert check_updated_dish_data['description'] == data_dishes_update['description']
    assert check_updated_dish_data['price'] == data_dishes_update['price']


def test_delete_dish(client: TestClient, saved_data: dict) -> None:
    menu_id = saved_data['menu']['id']
    submenu_id = saved_data['submenu']['id']
    dish_id = saved_data['dish']['id']

    delete_dish_response = client.delete(
        reverse(
            delete_dish_endpoint,
            menu_id=menu_id,
            submenu_id=submenu_id,
            dish_id=dish_id,
        )
    )
    assert delete_dish_response.status_code == 200, delete_dish_response.text
    assert delete_dish_response.json() == {
        'status': 'true',
        'message': 'The dish has been deleted',
    }
    check_dish_response = client.get(
        reverse(
            get_dish_endpoint, menu_id=menu_id, submenu_id=submenu_id, dish_id=dish_id
        )
    )
    assert check_dish_response.status_code == 404, check_dish_response.text
    assert check_dish_response.json() == {'detail': 'dish not found'}

    client.delete(reverse(delete_menu_endpoint, menu_id=menu_id))  # DELETE!
