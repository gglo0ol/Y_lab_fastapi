from tests.conftest import client


def test_get_all_menu_empty():
    """get a empty list"""
    response = client.get("/api/v1/menus/")
    assert response.status_code == 200, response.text
    data = response.json()
    assert data == []


def test_menu():
    """Test all menu function"""

    # get empty list
    test_get_all_menu_empty()

    # create a new menu and get json
    create_menu_response = client.post(
        "/api/v1/menus/",
        json={"title": "My menu 1", "description": "My menu description 1"},
    )
    assert create_menu_response.status_code == 201, create_menu_response.text
    data = create_menu_response.json()
    assert all(
        map(lambda item: item in data, ("id", "title", "description"))
    ), "error data"
    menu_id = data["id"]

    # Test list menu
    all_menu_response = client.get("/api/v1/menus/")
    assert all_menu_response.status_code == 200, all_menu_response.text
    assert all_menu_response.json() == [data]

    # Test menu
    get_menu_response = client.get(f"/api/v1/menus/{menu_id}")
    assert get_menu_response.status_code == 200, get_menu_response.text
    assert all(
        map(
            lambda item: item in get_menu_response.json(),
            ("id", "title", "description"),
        )
    )

    # Test update menu
    new_title, new_description = "My updated menu 1", "My updated menu description 1"

    update_menu_response = client.patch(
        f"/api/v1/menus/{menu_id}",
        json={
            "title": new_title,
            "description": new_description,
        },
    )
    assert update_menu_response.status_code == 200, update_menu_response.text
    new_data = update_menu_response.json()

    assert all(
        map(lambda item: item in new_data, ("id", "title", "description"))
    ), "error"
    assert new_data["title"] == new_title and new_data["description"] == new_description

    # Check updated menu
    get_updated_menu = client.get(f"/api/v1/menus/{menu_id}")
    assert get_updated_menu.status_code == 200, get_updated_menu.text
    updated_data = get_updated_menu.json()
    assert (
        updated_data["title"] == new_data["title"]
        and updated_data["description"] == new_data["description"]
    )

    # Test delete menu
    delete_menu_response = client.delete(f"/api/v1/menus/{menu_id}")
    assert delete_menu_response.status_code == 200, delete_menu_response.text
    assert delete_menu_response.json() == {
        "status": "true",
        "message": "The menu has been deleted",
    }

    # Test all menu empty list
    test_get_all_menu_empty()

    # Test menu
    get_menu_response = client.get(f"/api/v1/menus/{menu_id}")
    assert get_menu_response.status_code == 404, get_menu_response.text
    assert get_menu_response.json() == {"detail": "menu not found"}
