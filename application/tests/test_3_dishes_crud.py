import pytest
from fastapi.testclient import TestClient


from .test_1_menu_crud import create_menu
from .test_2_submenu_crud import create_submenu


json_dishes_create = {
    "title": "My dish 1",
    "description": "My dish description 1",
    "price": "12.50",
}

json_dishes_update = {
    "title": "My updated dish 1",
    "description": "My updated dish description 1",
    "price": "14.50",
}


@pytest.fixture
def create_dish(
    create_menu,
    create_submenu,
    client: TestClient,
    title: str = json_dishes_create["title"],
    description: str = json_dishes_create["description"],
    price: str = json_dishes_create["price"],
):
    menu_id = create_menu.json()["id"]
    submenu_id = create_submenu.json()["id"]
    response = client.post(
        f"/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes",
        json={"title": title, "description": description, "price": price},
    )
    return response


def create_dish_by_id(
    menu_id: str,
    submenu_id: str,
    client: TestClient,
    title: str = json_dishes_create["title"],
    description: str = json_dishes_create["description"],
    price: str = json_dishes_create["price"],
):
    response = client.post(
        f"/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes",
        json={"title": title, "description": description, "price": price},
    )
    return response


def get_all_dish(client: TestClient, submenu_id: str, menu_id: str):
    response = client.get(f"/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes")
    return response


def get_dish(client: TestClient, dish_id: str, submenu_id: str, menu_id: str):
    response = client.get(
        f"/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}"
    )
    return response


def update_dish(
    client: TestClient,
    dish_id: str,
    submenu_id: str,
    menu_id: str,
):
    response = client.patch(
        f"/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}",
        json={
            "title": json_dishes_update["title"],
            "description": json_dishes_update["description"],
            "price": json_dishes_update["price"],
        },
    )
    return response


def delete_dish(client: TestClient, dish_id: str, submenu_id: str, menu_id: str):
    response = client.delete(
        f"/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}"
    )
    return response


def test_get_empty_dishes_list(client: TestClient, create_menu, create_submenu):
    assert create_menu.status_code == 201, create_menu.text
    menu_id = create_menu.json()["id"]
    assert create_submenu.status_code == 201, create_submenu.text
    submenu_data = create_submenu.json()
    assert all(map(lambda item: item in submenu_data, ("id", "title", "description")))
    submenu_id = submenu_data["id"]
    all_dishes_list_response = get_all_dish(
        client=client, menu_id=menu_id, submenu_id=submenu_id
    )
    assert all_dishes_list_response.status_code == 200, all_dishes_list_response.text
    assert all_dishes_list_response.json() == []


def test_create_dish(create_dish):
    assert create_dish.status_code == 201, create_dish.text
    dish_data = create_dish.json()
    assert all(
        map(lambda item: item in dish_data, ("id", "title", "description", "price"))
    )
    assert dish_data["title"] == json_dishes_create["title"]
    assert dish_data["description"] == json_dishes_create["description"]
    assert dish_data["price"] == json_dishes_create["price"]


def test_not_empty_dishes_list(
    client: TestClient, create_menu, create_submenu, create_dish
):
    menu_id = create_menu.json()["id"]
    submenu_id = create_submenu.json()["id"]

    assert create_dish.status_code == 201, create_dish.text
    dish_data = create_dish.json()
    assert all(
        map(lambda item: item in dish_data, ("id", "title", "description", "price"))
    )
    check_not_empty_dishes_list = get_all_dish(
        client=client, menu_id=menu_id, submenu_id=submenu_id
    )
    assert (
        check_not_empty_dishes_list.status_code == 200
    ), check_not_empty_dishes_list.text
    assert check_not_empty_dishes_list.json() != []


def test_get_dish(client: TestClient, create_menu, create_submenu, create_dish):
    menu_id = create_menu.json()["id"]
    submenu_id = create_submenu.json()["id"]
    dish_id = create_dish.json()["id"]
    get_dish_response = get_dish(
        client=client, menu_id=menu_id, submenu_id=submenu_id, dish_id=dish_id
    )
    assert get_dish_response.status_code == 200, get_dish_response.text
    dish_data = get_dish_response.json()
    assert all(
        map(
            lambda item: item in dish_data,
            ("id", "title", "description", "price"),
        )
    )
    assert dish_data["title"] == json_dishes_create["title"]
    assert dish_data["description"] == json_dishes_create["description"]
    assert dish_data["price"] == json_dishes_create["price"]


def test_update_dish(client: TestClient, create_menu, create_submenu, create_dish):
    menu_id = create_menu.json()["id"]
    submenu_id = create_submenu.json()["id"]
    dish_id = create_dish.json()["id"]

    update_dish_response = update_dish(
        client=client, menu_id=menu_id, submenu_id=submenu_id, dish_id=dish_id
    )
    assert update_dish_response.status_code == 200, update_dish_response.text

    check_updated_dish = get_dish(
        client=client, menu_id=menu_id, submenu_id=submenu_id, dish_id=dish_id
    )
    assert check_updated_dish.status_code == 200, check_updated_dish.text
    check_updated_dish_data = check_updated_dish.json()
    assert all(
        map(
            lambda item: item in check_updated_dish_data,
            ("id", "title", "description", "price"),
        )
    )
    assert check_updated_dish_data["title"] == json_dishes_update["title"]
    assert check_updated_dish_data["description"] == json_dishes_update["description"]
    assert check_updated_dish_data["price"] == json_dishes_update["price"]


def test_delete_dish(client: TestClient, create_menu, create_submenu, create_dish):
    menu_id = create_menu.json()["id"]
    submenu_id = create_submenu.json()["id"]
    dish_id = create_dish.json()["id"]

    delete_dish_response = delete_dish(
        client=client, menu_id=menu_id, submenu_id=submenu_id, dish_id=dish_id
    )
    assert delete_dish_response.status_code == 200, delete_dish_response.text
    assert delete_dish_response.json() == {
        "status": "true",
        "message": "The dish has been deleted",
    }
    check_dish_response = get_dish(
        client=client, menu_id=menu_id, submenu_id=submenu_id, dish_id=dish_id
    )
    assert check_dish_response.status_code == 404, check_dish_response.text
    assert check_dish_response.json() == {"detail": "dish not found"}
