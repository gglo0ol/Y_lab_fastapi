from fastapi.testclient import TestClient


def create_menu(
    client: TestClient,
    title: str = "My menu 1",
    description: str = "My menu description 1",
):
    response = client.post(
        "/api/v1/menus/",
        json={"title": title, "description": description},
    )
    return response


def get_menu(menu_id: str, client: TestClient):
    response = client.get(f"/api/v1/menus/{menu_id}")
    return response


def get_all_menus(client: TestClient):
    response = client.get("/api/v1/menus/")
    return response


def update_menu(
    client: TestClient,
    menu_id: str,
    new_title="My updated menu 1",
    new_description="My updated menu description 1",
):
    response = client.patch(
        f"/api/v1/menus/{menu_id}",
        json={
            "title": new_title,
            "description": new_description,
        },
    )
    return response


def delete_menu(menu_id: str, client: TestClient):
    response = client.delete(f"/api/v1/menus/{menu_id}")
    return response


def test_menu_empty_list(client: TestClient):
    response = get_all_menus(client=client)
    assert response.status_code == 200, response.text
    assert response.json() == []


def test_create_menu(client: TestClient):
    response = create_menu(client=client)
    assert response.status_code == 201, response.text
    menu_data = response.json()
    assert all(map(lambda item: item in menu_data, ("id", "title", "description")))


def test_get_menu(client: TestClient):
    create_menu_response = create_menu(client=client)
    assert create_menu_response.status_code == 201, create_menu_response.text
    menu_id = create_menu_response.json()["id"]
    get_menu_response = get_menu(menu_id=menu_id, client=client)
    assert get_menu_response.status_code == 200, get_menu_response.text
    menu_data = get_menu_response.json()
    assert all(map(lambda item: item in menu_data, ("id", "title", "description")))


def test_menu_not_empty(client: TestClient):
    create_response = create_menu(client=client)
    assert create_response.status_code == 201, create_response.text
    menu_not_empty_list_response = get_all_menus(client=client)
    assert (
        menu_not_empty_list_response.status_code == 200
    ), menu_not_empty_list_response.text
    data = menu_not_empty_list_response.json()
    assert data != []


def test_menu_update(client: TestClient):
    create_menu_response = create_menu(client=client)
    assert create_menu_response.status_code == 201, create_menu_response.text
    menu_data = create_menu_response.json()
    menu_id = menu_data["id"]
    menu_response = get_menu(menu_id=menu_id, client=client)
    assert menu_data == menu_response.json()
    update_menu_response = update_menu(
        menu_id=menu_id,
        client=client,
    )
    assert update_menu_response.status_code == 200, update_menu_response.text
    updated_menu_data = update_menu_response.json()
    assert all(
        map(lambda item: item in updated_menu_data, ("id", "title", "description"))
    )
    menu_updated_response = get_menu(menu_id=menu_id, client=client)
    assert menu_updated_response.json() != menu_data


def test_delete_menu(client: TestClient):
    create_response = create_menu(client=client)
    assert create_response.status_code == 201, create_response.text
    menu_id = create_response.json()["id"]
    delete_response = delete_menu(menu_id=menu_id, client=client)
    assert delete_response.status_code == 200, delete_response.text
    assert delete_response.json() == {
        "status": "true",
        "message": "The menu has been deleted",
    }
    get_menu_response = get_menu(menu_id=menu_id, client=client)
    assert get_menu_response.status_code == 404, get_menu_response.text
    assert get_menu_response.json() == {"detail": "menu not found"}
