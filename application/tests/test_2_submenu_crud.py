from menus.views import create_menu_endpoint, delete_menu_endpoint
from submenus.views import (
    create_submenu_endpoint,
    delete_submenu_endpoint,
    get_all_submenu_endpoint,
    get_submenu_endpoint,
    update_submenu_endpoint,
)
from tests.conftest import reverse
from httpx import AsyncClient


async def test_submenu_empty_list(
    client: AsyncClient, saved_data: dict, data_menu_create: dict
) -> None:
    response_create_menu = await client.post(
        reverse(create_menu_endpoint), json=data_menu_create
    )
    menu_data = response_create_menu.json()
    menu_id = menu_data["id"]
    all_submenu_response = await client.get(
        reverse(get_all_submenu_endpoint, menu_id=menu_id)
    )
    assert all_submenu_response.status_code == 200, all_submenu_response.text
    assert all_submenu_response.json() == []
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


async def test_get_submenu(client: AsyncClient, saved_data: dict) -> None:
    menu_id = saved_data["menu"]["id"]
    submenu_data = saved_data["submenu"]
    submenu_id = submenu_data["id"]
    submenu_response = await client.get(
        reverse(get_submenu_endpoint, menu_id=menu_id, submenu_id=submenu_id)
    )
    assert submenu_response.status_code == 200, submenu_response.text
    assert submenu_response.json()["title"] == submenu_data["title"]
    assert submenu_response.json()["description"] == submenu_data["description"]


async def test_submenu_not_empty_list(client: AsyncClient, saved_data: dict) -> None:
    menu_id = saved_data["menu"]["id"]
    all_submenu_response = await client.get(
        reverse(get_all_submenu_endpoint, menu_id=menu_id)
    )
    assert all_submenu_response.status_code == 200, all_submenu_response.text
    assert all_submenu_response.json() != []


async def test_update_submenu(
    client: AsyncClient, data_submenu_update: dict, saved_data: dict
) -> None:
    menu_id = saved_data["menu"]["id"]
    submenu_data = saved_data["submenu"]
    submenu_id = submenu_data["id"]
    update_response = await client.patch(
        reverse(update_submenu_endpoint, menu_id=menu_id, submenu_id=submenu_id),
        json=data_submenu_update,
    )
    assert update_response.status_code == 200, update_response.text
    updated_data = update_response.json()
    assert all(
        map(
            lambda item: item in updated_data,
            ("id", "title", "description", "dishes_count"),
        )
    )
    assert updated_data != submenu_data
    assert updated_data["title"] == data_submenu_update["title"]
    assert updated_data["description"] == data_submenu_update["description"]


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
    check_submenu_response = await client.get(
        reverse(get_submenu_endpoint, menu_id=menu_id, submenu_id=submenu_id)
    )
    assert check_submenu_response.status_code == 404, check_submenu_response.text
    assert check_submenu_response.json() == {"detail": "submenu not found"}

    await client.delete(reverse(delete_menu_endpoint, menu_id=menu_id))  # delete!
