from menus.views import (
    create_menu_endpoint,
    delete_menu_endpoint,
    get_all_menus_endpoint,
    get_menu_endpoint,
    update_menu_endpoint,
)
from tests.conftest import reverse
from httpx import AsyncClient


async def test_menu_empty_list(client: AsyncClient) -> None:
    response = await client.get(reverse(get_all_menus_endpoint))
    assert response.status_code == 200, response.text
    assert response.json() == []


async def test_create_menu(client: AsyncClient, data_menu_create, saved_data) -> None:
    response = await client.post(reverse(create_menu_endpoint), json=data_menu_create)
    assert response.status_code == 201, response.text
    menu_data = response.json()
    assert all(map(lambda item: item in menu_data, ("id", "title", "description")))
    assert menu_data["title"] == data_menu_create["title"]
    assert menu_data["description"] == data_menu_create["description"]
    saved_data["menu"] = menu_data


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
    assert menu_data == saved_data["menu"]


async def test_menu_not_empty(client: AsyncClient) -> None:
    response_all_menus = await client.get(reverse(get_all_menus_endpoint))
    assert response_all_menus.status_code == 200, response_all_menus.text
    data = response_all_menus.json()
    assert data != []


async def test_menu_update(
    client: AsyncClient, saved_data: dict, data_menu_update: dict
) -> None:
    menu_data = saved_data["menu"]
    menu_id = menu_data["id"]
    update_menu_response = await client.patch(
        reverse(update_menu_endpoint, menu_id=menu_id), json=data_menu_update
    )
    assert update_menu_response.status_code == 200, update_menu_response.text
    menu_updated_response = await client.get(
        reverse(get_menu_endpoint, menu_id=menu_id)
    )
    updated_data = menu_updated_response.json()
    assert updated_data != menu_data
    assert updated_data["title"] == data_menu_update["title"]
    assert updated_data["description"] == data_menu_update["description"]
    saved_data["menu"] = updated_data


async def test_delete_menu(client: AsyncClient, saved_data: dict) -> None:
    menu_data = saved_data["menu"]
    menu_id = menu_data["id"]
    delete_response = await client.delete(
        reverse(delete_menu_endpoint, menu_id=menu_id)
    )
    assert delete_response.status_code == 200, delete_response.text
    assert delete_response.json() == {
        "status": "true",
        "message": "The menu has been deleted",
    }
    get_menu_response = await client.get(reverse(get_menu_endpoint, menu_id=menu_id))
    assert get_menu_response.status_code == 404, get_menu_response.text
    assert get_menu_response.json() == {"detail": "menu not found"}
