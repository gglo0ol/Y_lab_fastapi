from tests.conftest import client
from tests.test_menu_crud import create_menu, delete_menu, get_all_menus


def create_submenu(menu_id: str, title: str, description: str):
    response = client.post(
        f"/api/v1/menus/{menu_id}/submenus",
        json={"title": title, "description": description},
    )
    return response


def check_submenu(menu_id: str, submenu_id):
    response = client.get(f"/api/v1/menus/{menu_id}/submenus/{submenu_id}")
    return response


def check_all_submenu(menu_id: str):
    response = client.get(f"/api/v1/menus/{menu_id}/submenus")
    return response


def update_submenu(menu_id: str, submenu_id: str, title: str, description: str):
    response = client.patch(
        f"/api/v1/menus/{menu_id}/submenus/{submenu_id}",
        json={
            "title": title,
            "description": description,
        },
    )
    return response


def delete_submenu(menu_id: str, submenu_id: str):
    response = client.delete(f"/api/v1/menus/{menu_id}/submenus/{submenu_id}")
    return response


def test_submenu():
    # create menu
    create_menu_response = create_menu(
        title="My submenu 1", description="My submenu description 1"
    )
    assert create_menu_response.status_code == 201, create_menu_response.text
    menu_data = create_menu_response.json()
    assert "id" in menu_data
    menu_id = menu_data["id"]

    # Check list submenu (empty list)
    all_submenu_response = check_all_submenu(menu_id=menu_id)
    assert all_submenu_response.status_code == 200, all_submenu_response.text
    assert all_submenu_response.json() == []

    # Create submenu
    submenu_title, submenu_description = "My submenu 1", "My submenu description 1"
    create_submenu_response = create_submenu(
        menu_id=menu_id, title=submenu_title, description=submenu_description
    )
    assert create_submenu_response.status_code == 201, create_menu_response.text
    sub_data = create_submenu_response.json()
    assert all(map(lambda item: item in sub_data, ("title", "description")))
    assert "id" in sub_data
    submenu_id = sub_data["id"]

    # Test not empty list
    check_submenu_response = check_all_submenu(menu_id=menu_id)
    assert check_submenu_response.status_code == 200, check_submenu_response.text
    assert check_submenu_response.json() != []

    # Check submenu
    get_submenu_response = check_submenu(menu_id=menu_id, submenu_id=submenu_id)
    assert get_submenu_response.status_code == 200, get_submenu_response.text
    data = get_submenu_response.json()
    assert data["title"] == submenu_title and data["description"] == submenu_description

    # Update submenu
    new_title, new_description = (
        "My updated submenu 1",
        "My updated submenu description 1",
    )
    assert new_title != submenu_title and new_description != submenu_description
    sub_update = update_submenu(
        menu_id=menu_id,
        submenu_id=submenu_id,
        title=new_title,
        description=new_description,
    )
    assert sub_update.status_code == 200, sub_update.text
    update_data = sub_update.json()
    assert (
        update_data["title"] == new_title
        and update_data["description"] == new_description
    )

    # Check submenu
    check_sub_response = check_submenu(menu_id=menu_id, submenu_id=submenu_id)
    assert check_sub_response.status_code == 200, check_sub_response.text
    checked_data = check_sub_response.json()
    assert (
        update_data["id"] == checked_data["id"]
        and checked_data["title"] == new_title
        and checked_data["description"] == new_description
    )

    # Delete submenu
    delete_submenu_response = delete_submenu(menu_id=menu_id, submenu_id=submenu_id)
    assert delete_submenu_response.status_code == 200, delete_submenu_response.text

    # Check submenu list (is empty)
    check = check_all_submenu(menu_id=menu_id)
    assert check.status_code == 200, check.text
    assert check.json() == []

    # Check submenu
    sub = check_submenu(menu_id=menu_id, submenu_id=submenu_id)
    assert sub.status_code == 404, sub.text
    assert sub.json() == {"detail": "submenu not found"}

    # Delete menu
    menu_delete = delete_menu(menu_id=menu_id)
    assert menu_delete.status_code == 200, menu_delete.text

    # Check menu list (is empty)
    menu_check = get_all_menus()
    assert menu_check.status_code == 200, menu_check.text
    assert menu_check.json() == []
