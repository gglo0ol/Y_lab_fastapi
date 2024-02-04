from fastapi.testclient import TestClient

from menus.views import (
    create_menu_endpoint,
    get_all_menus_endpoint,
    get_menu_endpoint,
    update_menu_endpoint,
    delete_menu_endpoint,
)
from tests.conftest import reverse


# def create_menu_by_id(
#     client: TestClient,
#     data_create_menu: dict,
# ):
#     response = client.post("/api/v1/menus/", json=data_create_menu)
#     return response
#
#
# def create_menu(
#     client: TestClient,
#     data_create_menu: dict,
# ):
#     response = client.post("/api/v1/menus/", json=data_create_menu)
#     return response
#
#
# def get_all_menus(client: TestClient):
#     response = client.get("/api/v1/menus/")
#     return response
#
#
# def get_menu(menu_id: str, client: TestClient):
#     response = client.get(f"/api/v1/menus/{menu_id}")
#     return response
#
#
# def update_menu(
#     menu_id,
#     client: TestClient,
#     data_update_menu: dict,
# ):
#     response = client.patch(f"/api/v1/menus/{menu_id}", json=data_update_menu)
#     return response
#
#
# def delete_menu(menu_id: str, client: TestClient):
#     response = client.delete(f"/api/v1/menus/{menu_id}")
#     return response


def test_menu_empty_list(client: TestClient):
    response = client.get(reverse(get_all_menus_endpoint))
    assert response.status_code == 200, response.text
    assert response.json() == []


def test_create_menu(client: TestClient, data_menu_create, saved_data):
    response = client.post(reverse(create_menu_endpoint), json=data_menu_create)
    assert response.status_code == 201, response.text
    menu_data = response.json()
    assert all(map(lambda item: item in menu_data, ("id", "title", "description")))
    assert menu_data["title"] == data_menu_create["title"]
    assert menu_data["description"] == data_menu_create["description"]
    saved_data["menu"] = menu_data


def test_get_menu(client: TestClient, saved_data):
    menu_id = saved_data["menu"]["id"]
    response = client.get(reverse(get_menu_endpoint, menu_id=menu_id))
    assert response.status_code == 200, response.text
    menu_data = response.json()
    assert all(map(lambda item: item in menu_data, ("id", "title", "description")))
    assert menu_data == saved_data["menu"]


def test_menu_not_empty(client: TestClient, create_menu, get_all_menus):
    assert create_menu.status_code == 201, create_menu.text
    assert get_all_menus.status_code == 200, get_all_menus.text
    data = get_all_menus.json()
    assert data != []


def test_menu_update(client: TestClient, create_menu):
    assert create_menu.status_code == 201, create_menu.text
    menu_data = create_menu.json()
    assert menu_data["title"] == json_create_menu["title"]
    assert menu_data["description"] == json_create_menu["description"]
    menu_id = menu_data["id"]
    menu_response = get_menu(menu_id=menu_id, client=client)
    assert menu_data == menu_response.json()
    update_menu_response = update_menu(menu_id=menu_id, client=client)
    assert update_menu_response.status_code == 200, update_menu_response.text
    updated_menu_data = update_menu_response.json()
    assert all(
        map(lambda item: item in updated_menu_data, ("id", "title", "description"))
    )
    menu_updated_response = get_menu(menu_id=menu_id, client=client)
    assert menu_updated_response.json() != menu_data
    assert updated_menu_data["title"] == json_update_menu["title"]
    assert updated_menu_data["description"] == json_update_menu["description"]


def test_delete_menu(client: TestClient, create_menu):
    assert create_menu.status_code == 201, create_menu.text
    menu_id = create_menu.json()["id"]
    delete_response = delete_menu(menu_id=menu_id, client=client)
    assert delete_response.status_code == 200, delete_response.text
    assert delete_response.json() == {
        "status": "true",
        "message": "The menu has been deleted",
    }
    get_menu_response = get_menu(menu_id=menu_id, client=client)
    assert get_menu_response.status_code == 404, get_menu_response.text
    assert get_menu_response.json() == {"detail": "menu not found"}
