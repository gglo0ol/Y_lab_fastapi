import pytest
from fastapi.testclient import TestClient

from .test_1_menu_crud import create_menu

json_submenu_create = {
    "title": "My submenu 1",
    "description": "My submenu description 1",
}
json_submenu_update = {
    "title": "My updated submenu 1",
    "description": "My updated submenu description 1",
}


@pytest.fixture
def create_submenu(
    create_menu,
    client: TestClient,
):
    menu_id = create_menu.json()["id"]
    response = client.post(
        f"/api/v1/menus/{menu_id}/submenus", json=json_submenu_create
    )
    return response


def create_submenu_by_id(
    menu_id,
    client: TestClient,
):
    response = client.post(
        f"/api/v1/menus/{menu_id}/submenus", json=json_submenu_create
    )
    return response


def get_submenu(client: TestClient, menu_id: str, submenu_id: str):
    response = client.get(f"/api/v1/menus/{menu_id}/submenus/{submenu_id}")
    return response


def get_all_submenu(client: TestClient, menu_id: str):
    response = client.get(f"/api/v1/menus/{menu_id}/submenus")
    return response


def update_submenu(
    client: TestClient,
    menu_id: str,
    submenu_id: str,
):
    response = client.patch(
        f"/api/v1/menus/{menu_id}/submenus/{submenu_id}", json=json_submenu_update
    )
    return response


def delete_submenu(client: TestClient, menu_id: str, submenu_id: str):
    response = client.delete(f"/api/v1/menus/{menu_id}/submenus/{submenu_id}")
    return response


def test_submenu_empty_list(client: TestClient, create_menu):
    assert create_menu.status_code == 201, create_menu.text
    menu_id = create_menu.json()["id"]
    all_submenu_response = get_all_submenu(client=client, menu_id=menu_id)
    assert all_submenu_response.status_code == 200, all_submenu_response.text
    assert all_submenu_response.json() == []


def test_create_submenu(create_menu, create_submenu):
    submenu_data = create_submenu.json()
    assert all(map(lambda item: item in submenu_data, ("id", "title", "description")))
    assert submenu_data["title"] == json_submenu_create["title"]
    assert submenu_data["description"] == json_submenu_create["description"]


def test_get_submenu(client: TestClient, create_menu, create_submenu):
    menu_id = create_menu.json()["id"]
    submenu_data = create_submenu.json()
    submenu_id = submenu_data["id"]
    assert all(map(lambda item: item in submenu_data, ("id", "title", "description")))
    get_submenu_response = get_submenu(
        client=client, menu_id=menu_id, submenu_id=submenu_id
    )
    assert get_submenu_response.status_code == 200, get_submenu_response.text
    assert get_submenu_response.json() == submenu_data
    assert get_submenu_response.json()["title"] == json_submenu_create["title"]
    assert (
        get_submenu_response.json()["description"] == json_submenu_create["description"]
    )


def test_submenu_not_empty_list(client: TestClient, create_menu, create_submenu):
    menu_id = create_menu.json()["id"]
    assert create_submenu.status_code == 201, create_submenu.text
    submenu_data = create_submenu.json()
    assert all(map(lambda item: item in submenu_data, ("id", "title", "description")))
    all_submenu_response = get_all_submenu(client=client, menu_id=menu_id)
    assert all_submenu_response.status_code == 200, all_submenu_response.text
    assert all_submenu_response.json() != []


def test_update_submenu(client: TestClient, create_submenu, create_menu):
    assert create_menu.status_code == 201, create_menu.text
    menu_id = create_menu.json()["id"]
    assert create_submenu.status_code == 201, create_submenu.text
    submenu_data = create_submenu.json()
    assert all(map(lambda item: item in submenu_data, ("id", "title", "description")))
    submenu_id = submenu_data["id"]
    update_response = update_submenu(
        client=client, menu_id=menu_id, submenu_id=submenu_id
    )
    assert update_response.status_code == 200, update_response.text
    updated_data = update_response.json()
    assert all(map(lambda item: item in updated_data, ("id", "title", "description")))
    assert updated_data != submenu_data
    assert updated_data["title"] == json_submenu_update["title"]
    assert updated_data["description"] == json_submenu_update["description"]


def test_delete_submenu(client: TestClient, create_submenu, create_menu):
    assert create_menu.status_code == 201, create_menu.text
    menu_id = create_menu.json()["id"]
    assert create_submenu.status_code == 201, create_submenu.text
    submenu_data = create_submenu.json()
    assert all(map(lambda item: item in submenu_data, ("id", "title", "description")))
    submenu_id = submenu_data["id"]
    delete_submenu_response = delete_submenu(
        client=client, menu_id=menu_id, submenu_id=submenu_id
    )
    assert delete_submenu_response.status_code == 200, delete_submenu_response.text
    assert delete_submenu_response.json() == {
        "status": "true",
        "message": "The submenu has been deleted",
    }
    check_submenu_response = get_submenu(
        client=client, menu_id=menu_id, submenu_id=submenu_id
    )
    assert check_submenu_response.status_code == 404, check_submenu_response.text
    assert check_submenu_response.json() == {"detail": "submenu not found"}
