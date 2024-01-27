from tests.conftest import client


def test_get_all_menu_empty():
    response = client.get("/api/v1/menus/")
    assert response.status_code == 200, response.text
    data = response.json()
    assert data == []


def test_menu():
    test_get_all_menu_empty()
    create_menu_response = client.post(
        "/api/v1/menus/",
        json={"title": "My menu 1", "description": "My menu description 1"},
    )
    assert create_menu_response.status_code == 201, create_menu_response.text
    data = create_menu_response.json()
    assert "id" in data
    menu_id = data["id"]
    all_menu_response = client.get("/api/v1/menus/")
    assert all_menu_response.json() == [data]
    get_menu_response = client.get(f"/api/v1/menus/{menu_id}")
    assert get_menu_response.json() == data
    update_menu_response = client.patch(
        f"/api/v1/menus/{menu_id}",
        json={
            "title": "My updated menu 1",
            "description": "My updated menu description 1",
        },
    )
    get_updated_menu_response = client.get(f"/api/v1/menus/{menu_id}")
    assert update_menu_response.json() == get_updated_menu_response.json()
    delete_menu_response = client.delete(f"/api/v1/menus/{menu_id}")
    assert delete_menu_response.status_code == 200, delete_menu_response.text
    assert delete_menu_response.json() == {
        "status": "true",
        "message": "The menu has been deleted",
    }
    test_get_all_menu_empty()
    get_menu_response = client.get(f"/api/v1/menus/{menu_id}")
    assert get_menu_response.status_code == 404, get_updated_menu_response.text
    assert get_menu_response.json() == {"detail": "menu not found"}


def test_submenu():
    create_menu_response = client.post(
        "/api/v1/menus/",
        json={"title": "My menu 1", "description": "My menu description 1"},
    )
    assert create_menu_response.status_code == 201, create_menu_response.text
    data = create_menu_response.json()
    assert "id" in data
    menu_id = data["id"]
    all_menu_response = client.get("/api/v1/menus/")
    assert all_menu_response.json() == [data]
    create_submenu_response = client.post(
        f"/api/v1/menus/{menu_id}",
        json={"title": "My submenu 1", "description": "My submenu description 1"},
    )
    assert create_submenu_response.status_code == 201, create_menu_response.text
    data = create_menu_response.json()
    assert "id" in data
    submenu_id = data["id"]
