from dishes.views import create_dish_endpoint, get_all_dishes_endpoint
from menus.views import (
    create_menu_endpoint,
    delete_menu_endpoint,
    get_all_menus_endpoint,
    get_menu_endpoint,
)
from submenus.views import (
    create_submenu_endpoint,
    delete_submenu_endpoint,
    get_all_submenu_endpoint,
    get_submenu_endpoint,
)
from tests.conftest import reverse
from httpx import AsyncClient


async def test_create_menu(client: AsyncClient, data_menu_create, saved_data) -> None:
    response = await client.post(reverse(create_menu_endpoint), json=data_menu_create)
    assert response.status_code == 201, response.text
    menu_data = response.json()
    assert all(map(lambda item: item in menu_data, ("id", "title", "description")))
    assert menu_data["title"] == data_menu_create["title"]
    assert menu_data["description"] == data_menu_create["description"]
    saved_data["menu"] = menu_data


async def test_create_submenu(
    client: AsyncClient, saved_data: dict, data_submenu_create: dict
) -> None:
    menu_id = saved_data["menu"]["id"]
    create_submenu_response = await client.post(
        reverse(create_submenu_endpoint, menu_id=menu_id), json=data_submenu_create
    )
    assert create_submenu_response.status_code == 201, create_submenu_response.text
    data_submenu = create_submenu_response.json()
    assert all(
        map(
            lambda item: item in data_submenu,
            ("id", "title", "description", "dishes_count"),
        )
    )
    assert data_submenu["title"] == data_submenu_create["title"]
    assert data_submenu["description"] == data_submenu_create["description"]
    saved_data["submenu"] = data_submenu


async def test_create_dish_1(
    client: AsyncClient,
    saved_data: dict,
) -> None:
    json_dish_1 = {
        "title": "My dish 2",
        "description": "My dish description 2",
        "price": "13.50",
        "discount": 0,
    }
    menu_id = saved_data["menu"]["id"]
    submenu_id = saved_data["submenu"]["id"]
    dish_create_response = await client.post(
        reverse(create_dish_endpoint, menu_id=menu_id, submenu_id=submenu_id),
        json=json_dish_1,
    )
    assert dish_create_response.status_code == 201, dish_create_response.text
    dish_data = dish_create_response.json()
    assert all(
        map(lambda item: item in dish_data, ("id", "title", "description", "price"))
    )
    assert dish_data["title"] == json_dish_1["title"]
    assert dish_data["description"] == json_dish_1["description"]
    assert dish_data["price"] == json_dish_1["price"]
    assert dish_data["discount"] == json_dish_1["discount"]
    saved_data["dish_1"] = dish_data


async def test_create_dish_2(
    client: AsyncClient, saved_data: dict, data_dishes_create: dict
) -> None:
    menu_id = saved_data["menu"]["id"]
    submenu_id = saved_data["submenu"]["id"]
    dish_create_response = await client.post(
        reverse(create_dish_endpoint, menu_id=menu_id, submenu_id=submenu_id),
        json=data_dishes_create,
    )
    assert dish_create_response.status_code == 201, dish_create_response.text
    dish_data = dish_create_response.json()
    assert all(
        map(lambda item: item in dish_data, ("id", "title", "description", "price"))
    )
    assert dish_data["title"] == data_dishes_create["title"]
    assert dish_data["description"] == data_dishes_create["description"]
    assert dish_data["price"] == data_dishes_create["price"]
    saved_data["dish_2"] = dish_data


async def test_check_menu(client: AsyncClient, saved_data) -> None:
    menu_id = saved_data["menu"]["id"]
    response = await client.get(reverse(get_menu_endpoint, menu_id=menu_id))
    assert response.status_code == 200, response.text
    check_menu_data = response.json()
    assert all(
        map(
            lambda item: item in check_menu_data,
            ("id", "title", "description", "dishes_count", "submenus_count"),
        )
    )
    assert check_menu_data["id"] == menu_id
    assert check_menu_data["dishes_count"] == 2
    assert check_menu_data["submenus_count"] == 1


async def test_check_submenu(client: AsyncClient, saved_data: dict) -> None:
    menu_id = saved_data["menu"]["id"]
    submenu_id = saved_data["submenu"]["id"]
    submenu_response = await client.get(
        reverse(get_submenu_endpoint, menu_id=menu_id, submenu_id=submenu_id)
    )
    assert submenu_response.status_code == 200, submenu_response.text
    check_submenu_data = submenu_response.json()
    assert check_submenu_data["id"] == submenu_id
    assert check_submenu_data["dishes_count"] == 2


async def test_delete_submenu(client: AsyncClient, saved_data: dict) -> None:
    menu_id = saved_data["menu"]["id"]
    submenu_id = saved_data["submenu"]["id"]
    delete_submenu_response = await client.delete(
        reverse(delete_submenu_endpoint, menu_id=menu_id, submenu_id=submenu_id)
    )
    assert delete_submenu_response.status_code == 200, delete_submenu_response.text
    assert delete_submenu_response.json() == {
        "status": "true",
        "message": "The submenu has been deleted",
    }


async def test_submenu_empty_list(
    client: AsyncClient, saved_data: dict, data_menu_create: dict
) -> None:
    menu_id = saved_data["menu"]["id"]
    all_submenu_response = await client.get(
        reverse(get_all_submenu_endpoint, menu_id=menu_id)
    )
    assert all_submenu_response.status_code == 200, all_submenu_response.text
    assert all_submenu_response.json() == []


async def test_get_empty_dishes_list(
    client: AsyncClient,
    saved_data: dict,
) -> None:
    menu_id = saved_data["menu"]["id"]
    submenu_id = saved_data["submenu"]["id"]
    all_dishes_list_response = await client.get(
        reverse(get_all_dishes_endpoint, menu_id=menu_id, submenu_id=submenu_id)
    )
    assert all_dishes_list_response.status_code == 200, all_dishes_list_response.text
    assert all_dishes_list_response.json() == []


async def test_get_menu(client: AsyncClient, saved_data) -> None:
    menu_id = saved_data["menu"]["id"]
    response = await client.get(reverse(get_menu_endpoint, menu_id=menu_id))
    assert response.status_code == 200, response.text
    menu_data = response.json()
    assert all(
        map(
            lambda item: item in menu_data,
            ("id", "title", "description", "dishes_count", "submenus_count"),
        )
    )
    assert menu_data["dishes_count"] == 0
    assert menu_data["submenus_count"] == 0


async def test_delete_menu(client: AsyncClient, saved_data: dict) -> None:
    menu_data = saved_data["menu"]
    menu_id = menu_data["id"]
    delete_response = await client.delete(
        reverse(delete_menu_endpoint, menu_id=menu_id)
    )
    assert delete_response.status_code == 200, delete_response.text


async def test_all_menu_empty_list(client: AsyncClient) -> None:
    response = await client.get(reverse(get_all_menus_endpoint))
    assert response.status_code == 200, response.text
    assert response.json() == []
