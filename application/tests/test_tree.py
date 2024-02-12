from dishes.views import create_dish_endpoint
from menus.views import (
    create_menu_endpoint,
    delete_menu_endpoint,
    menu_submenu_dishes,
)
from submenus.views import (
    create_submenu_endpoint,
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
    saved_data["dish_1"] = dish_data


async def test_tree(
    client: AsyncClient,
    saved_data: dict,
):
    menu_id = saved_data["menu"]["id"]
    submenu_id = saved_data["submenu"]["id"]
    tree_response = await client.get(reverse(menu_submenu_dishes))
    assert tree_response.status_code == 200, tree_response.text
    data_tree = tree_response.json()
    assert isinstance(data_tree, list)
    for menu in data_tree:
        assert menu["id"] == menu_id
        assert menu["title"] == saved_data["menu"]["title"]
        assert menu["description"] == saved_data["menu"]["description"]
        for submenu in menu["submenus"]:
            assert submenu["id"] == submenu_id
            assert submenu["title"] == saved_data["submenu"]["title"]
            assert submenu["description"] == saved_data["submenu"]["description"]
            for dish in submenu["dishes"]:
                assert dish["id"] == saved_data["dish_1"]["id"]
                assert dish["title"] == saved_data["dish_1"]["title"]
                assert dish["description"] == saved_data["dish_1"]["description"]


async def test_delete_menu(
    client: AsyncClient,
    saved_data: dict,
):
    menu_id = saved_data["menu"]["id"]
    delete_response = await client.delete(
        reverse(delete_menu_endpoint, menu_id=menu_id)
    )
    assert delete_response.status_code == 200, delete_response.text
