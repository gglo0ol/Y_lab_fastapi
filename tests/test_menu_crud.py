from tests.conftest import client


def create_menu(title: str, description: str):
    response = client.post(
        "/api/v1/menus/",
        json={"title": title, "description": description},
    )
    return response


def check_menu(menu_id: str):
    response = client.get(f"/api/v1/menus/{menu_id}")
    return response


def get_all_menus():
    response = client.get("/api/v1/menus/")
    return response


def update_menu(menu_id: str, new_title: str, new_description: str):
    response = client.patch(
        f"/api/v1/menus/{menu_id}",
        json={
            "title": new_title,
            "description": new_description,
        },
    )
    return response


def delete_menu(menu_id: str):
    response = client.delete(f"/api/v1/menus/{menu_id}")
    return response


def test_menu():
    """Test all menu function"""

    # get empty list
    get_empty_list = get_all_menus()
    assert get_empty_list.status_code == 200, get_empty_list.text
    assert get_empty_list.json() == []

    # create a new menu
    add_menu = create_menu(title="My menu 1", description="My menu description 1")
    assert add_menu.status_code == 201, add_menu.text
    data = add_menu.json()
    assert all(
        map(lambda item: item in data, ("id", "title", "description"))
    ), "error data"
    menu_id = data["id"]

    # Test list menu
    all_menu_response = get_all_menus()
    assert all_menu_response.status_code == 200, all_menu_response.text
    assert all_menu_response.json() != []

    # Test menu
    get_menu_response = check_menu(menu_id=menu_id)
    assert get_menu_response.status_code == 200, get_menu_response.text
    assert all(
        map(
            lambda item: item in get_menu_response.json(),
            ("id", "title", "description"),
        )
    )

    # Test update menu
    new_title, new_description = "My updated menu 1", "My updated menu description 1"

    update_menu_response = update_menu(
        menu_id=menu_id, new_title=new_title, new_description=new_description
    )
    assert update_menu_response.status_code == 200, update_menu_response.text
    new_data = update_menu_response.json()

    assert all(
        map(lambda item: item in new_data, ("id", "title", "description"))
    ), "error"
    assert new_data["title"] == new_title and new_data["description"] == new_description

    # Check updated menu
    get_updated_menu = check_menu(menu_id=menu_id)
    assert get_updated_menu.status_code == 200, get_updated_menu.text
    updated_data = get_updated_menu.json()
    assert (
        updated_data["title"] == new_data["title"]
        and updated_data["description"] == new_data["description"]
    )

    # Test delete menu
    delete_menu_response = delete_menu(menu_id=menu_id)
    assert delete_menu_response.status_code == 200, delete_menu_response.text
    assert delete_menu_response.json() == {
        "status": "true",
        "message": "The menu has been deleted",
    }

    # Test all menu empty list
    empty_list = get_all_menus()
    assert empty_list.status_code == 200, get_empty_list.text
    assert empty_list.json() == []

    # Test menu
    get_menu_response = check_menu(menu_id=menu_id)
    assert get_menu_response.status_code == 404, get_menu_response.text
    assert get_menu_response.json() == {"detail": "menu not found"}
