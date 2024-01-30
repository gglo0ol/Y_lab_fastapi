from fastapi.testclient import TestClient

from .test_1_menu_crud import create_menu


def create_submenu(
    client: TestClient,
    menu_id: str,
    title: str = "My submenu 1",
    description: str = "My submenu description 1",
):
    response = client.post(
        f"/api/v1/menus/{menu_id}/submenus",
        json={"title": title, "description": description},
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
    title: str = "My updated submenu 1",
    description: str = "My updated submenu description 1",
):
    response = client.patch(
        f"/api/v1/menus/{menu_id}/submenus/{submenu_id}",
        json={
            "title": title,
            "description": description,
        },
    )
    return response


def delete_submenu(client: TestClient, menu_id: str, submenu_id: str):
    response = client.delete(f"/api/v1/menus/{menu_id}/submenus/{submenu_id}")
    return response


def test_submenu_empty_list(client: TestClient):
    create_menu_response = create_menu(client=client)
    assert create_menu_response.status_code == 201, create_menu_response.text
    menu_id = create_menu_response.json()["id"]
    all_submenu_response = get_all_submenu(client=client, menu_id=menu_id)
    assert all_submenu_response.status_code == 200, all_submenu_response.text
    assert all_submenu_response.json() == []


def test_create_submenu(client: TestClient):
    create_menu_response = create_menu(client=client)
    assert create_menu_response.status_code == 201, create_menu_response.text
    menu_id = create_menu_response.json()["id"]
    create_submenu_response = create_submenu(client=client, menu_id=menu_id)
    assert create_submenu_response.status_code == 201, create_submenu_response.text
    submenu_data = create_submenu_response.json()
    assert all(map(lambda item: item in submenu_data, ("id", "title", "description")))


def test_get_submenu(client: TestClient):
    create_menu_response = create_menu(client=client)
    assert create_menu_response.status_code == 201, create_menu_response.text
    menu_id = create_menu_response.json()["id"]
    create_submenu_response = create_submenu(client=client, menu_id=menu_id)
    assert create_submenu_response.status_code == 201, create_submenu_response.text
    submenu_data = create_submenu_response.json()
    submenu_id = submenu_data["id"]
    assert all(map(lambda item: item in submenu_data, ("id", "title", "description")))
    get_submenu_response = get_submenu(
        client=client, menu_id=menu_id, submenu_id=submenu_id
    )
    assert get_submenu_response.status_code == 200, get_submenu_response.text
    assert get_submenu_response.json() == submenu_data


def test_submenu_not_empty_list(client: TestClient):
    create_menu_response = create_menu(client=client)
    assert create_menu_response.status_code == 201, create_menu_response.text
    menu_id = create_menu_response.json()["id"]
    create_submenu_response = create_submenu(client=client, menu_id=menu_id)
    assert create_submenu_response.status_code == 201, create_submenu_response.text
    submenu_data = create_submenu_response.json()
    assert all(map(lambda item: item in submenu_data, ("id", "title", "description")))
    all_submenu_response = get_all_submenu(client=client, menu_id=menu_id)
    assert all_submenu_response.status_code == 200, all_submenu_response.text
    assert all_submenu_response.json() != []


def test_update_submenu(client: TestClient):
    create_menu_response = create_menu(client=client)
    assert create_menu_response.status_code == 201, create_menu_response.text
    menu_id = create_menu_response.json()["id"]
    create_submenu_response = create_submenu(client=client, menu_id=menu_id)
    assert create_submenu_response.status_code == 201, create_submenu_response.text
    submenu_data = create_submenu_response.json()
    assert all(map(lambda item: item in submenu_data, ("id", "title", "description")))
    submenu_id = submenu_data["id"]
    all_submenu_response = get_all_submenu(client=client, menu_id=menu_id)
    assert all_submenu_response.status_code == 200, all_submenu_response.text
    assert all_submenu_response.json() != []
    update_response = update_submenu(
        client=client, menu_id=menu_id, submenu_id=submenu_id
    )
    assert update_response.status_code == 200, update_response.text
    updated_data = update_response.json()
    assert all(map(lambda item: item in updated_data, ("id", "title", "description")))
    assert updated_data != submenu_data


def test_delete_submenu(client: TestClient):
    create_menu_response = create_menu(client=client)
    assert create_menu_response.status_code == 201, create_menu_response.text
    menu_id = create_menu_response.json()["id"]
    create_submenu_response = create_submenu(client=client, menu_id=menu_id)
    assert create_submenu_response.status_code == 201, create_submenu_response.text
    submenu_data = create_submenu_response.json()
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
