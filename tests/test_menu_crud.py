from tests.conftest import client, test_get_db


"""def test_create_user():
    response = client.post(
        "/users/",
        json={"email": "deadpool@example.com", "password": "chimichangas4life"},
    )
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["email"] == "deadpool@example.com"
    assert "id" in data
    user_id = data["id"]

    response = client.get(f"/users/{user_id}")
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["email"] == "deadpool@example.com"
    assert data["id"] == user_id"""


def test_get_all_menus():
    response = client.get("/api/v1/menus/")
    assert response.status_code == 200, response.text
    data = response.json()
    assert data == []


def test_menus():
    response = client.post(
        "/api/v1/menus/",
        json={"title": "My menu 1", "description": "My menu description 1"},
    )
    assert response.status_code == 201, response.text
    data = response.json()
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
    assert delete_menu_response.status_code == 200, response.text
    assert delete_menu_response.json() == {
        "status": "true",
        "message": "The menu has been deleted",
    }
