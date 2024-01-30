from fastapi.testclient import TestClient


from .test_1_menu_crud import create_menu
from .test_2_submenu_crud import create_submenu


def create_dish(
    client: TestClient,
    submenu_id: str,
    menu_id: str,
    title: str = "My dish 1",
    description: str = "My dish description 1",
    price: str = "12.50",
):
    response = client.post(
        f"/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes",
        json={
            "menu_id": menu_id,
            "submenu_id": submenu_id,
            "title": title,
            "description": description,
            "price": price,
        },
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
    title: str = "My updated dish 1",
    description: str = "My updated dish description 1",
    price: str = "14.50",
):
    response = client.patch(
        f"/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}",
        json={
            "title": title,
            "description": description,
            "price": price,
        },
    )
    return response


def delete_dish(client: TestClient, dish_id: str, submenu_id: str, menu_id: str):
    response = client.delete(
        f"/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}"
    )
    return response


def test_get_empty_dishes_list(client: TestClient):
    create_menu_response = create_menu(client=client)
    assert create_menu_response.status_code == 201, create_menu_response.text
    menu_id = create_menu_response.json()["id"]
    create_submenu_response = create_submenu(client=client, menu_id=menu_id)
    assert create_submenu_response.status_code == 201, create_submenu_response.text
    submenu_data = create_submenu_response.json()
    assert all(map(lambda item: item in submenu_data, ("id", "title", "description")))
    submenu_id = submenu_data["id"]
    all_dishes_list_response = get_all_dish(
        client=client, menu_id=menu_id, submenu_id=submenu_id
    )
    assert all_dishes_list_response.status_code == 200, all_dishes_list_response.text
    assert all_dishes_list_response.json() == []


def test_create_dish(client: TestClient):
    create_menu_response = create_menu(client=client)
    assert create_menu_response.status_code == 201, create_menu_response.text
    menu_id = create_menu_response.json()["id"]
    create_submenu_response = create_submenu(client=client, menu_id=menu_id)
    assert create_submenu_response.status_code == 201, create_submenu_response.text
    submenu_data = create_submenu_response.json()
    assert all(map(lambda item: item in submenu_data, ("id", "title", "description")))
    submenu_id = submenu_data["id"]

    create_dish_response = create_dish(
        client=client, menu_id=menu_id, submenu_id=submenu_id
    )
    assert create_dish_response.status_code == 201, create_dish_response.text
    dish_data = create_dish_response.json()
    assert all(
        map(lambda item: item in dish_data, ("id", "title", "description", "price"))
    )


def test_not_empty_dishes_list(client: TestClient):
    create_menu_response = create_menu(client=client)
    assert create_menu_response.status_code == 201, create_menu_response.text
    menu_id = create_menu_response.json()["id"]
    create_submenu_response = create_submenu(client=client, menu_id=menu_id)
    assert create_submenu_response.status_code == 201, create_submenu_response.text
    submenu_data = create_submenu_response.json()
    assert all(map(lambda item: item in submenu_data, ("id", "title", "description")))
    submenu_id = submenu_data["id"]

    create_dish_response = create_dish(
        client=client, menu_id=menu_id, submenu_id=submenu_id
    )
    assert create_dish_response.status_code == 201, create_dish_response.text
    dish_data = create_dish_response.json()
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


def test_get_dish(client: TestClient):
    create_menu_response = create_menu(client=client)
    assert create_menu_response.status_code == 201, create_menu_response.text
    menu_id = create_menu_response.json()["id"]
    create_submenu_response = create_submenu(client=client, menu_id=menu_id)
    assert create_submenu_response.status_code == 201, create_submenu_response.text
    submenu_data = create_submenu_response.json()
    assert all(map(lambda item: item in submenu_data, ("id", "title", "description")))
    submenu_id = submenu_data["id"]

    create_dish_response = create_dish(
        client=client, menu_id=menu_id, submenu_id=submenu_id
    )
    assert create_dish_response.status_code == 201, create_dish_response.text
    dish_data = create_dish_response.json()
    assert all(
        map(lambda item: item in dish_data, ("id", "title", "description", "price"))
    )
    dish_id = dish_data["id"]
    get_dish_response = get_dish(
        client=client, menu_id=menu_id, submenu_id=submenu_id, dish_id=dish_id
    )
    assert get_dish_response.status_code == 200, get_dish_response.text
    geted_dish_data = get_dish_response.json()
    assert all(
        map(
            lambda item: item in geted_dish_data,
            ("id", "title", "description", "price"),
        )
    )
    assert geted_dish_data == dish_data


def test_update_dish(client: TestClient):
    create_menu_response = create_menu(client=client)
    assert create_menu_response.status_code == 201, create_menu_response.text
    menu_id = create_menu_response.json()["id"]
    create_submenu_response = create_submenu(client=client, menu_id=menu_id)
    assert create_submenu_response.status_code == 201, create_submenu_response.text
    submenu_data = create_submenu_response.json()
    assert all(map(lambda item: item in submenu_data, ("id", "title", "description")))
    submenu_id = submenu_data["id"]

    create_dish_response = create_dish(
        client=client, menu_id=menu_id, submenu_id=submenu_id
    )
    assert create_dish_response.status_code == 201, create_dish_response.text
    dish_data = create_dish_response.json()
    assert all(
        map(lambda item: item in dish_data, ("id", "title", "description", "price"))
    )
    dish_id = dish_data["id"]
    get_dish_response = get_dish(
        client=client, menu_id=menu_id, submenu_id=submenu_id, dish_id=dish_id
    )
    assert get_dish_response.status_code == 200, get_dish_response.text
    update_dish_response = update_dish(
        client=client, menu_id=menu_id, submenu_id=submenu_id, dish_id=dish_id
    )
    assert update_dish_response.status_code == 200, update_dish_response.text
    update_dish_data = update_dish_response.json()
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
    assert check_updated_dish_data == update_dish_data


def test_delete_dish(client: TestClient):
    create_menu_response = create_menu(client=client)
    assert create_menu_response.status_code == 201, create_menu_response.text
    menu_id = create_menu_response.json()["id"]
    create_submenu_response = create_submenu(client=client, menu_id=menu_id)
    assert create_submenu_response.status_code == 201, create_submenu_response.text
    submenu_data = create_submenu_response.json()
    assert all(map(lambda item: item in submenu_data, ("id", "title", "description")))
    submenu_id = submenu_data["id"]

    create_dish_response = create_dish(
        client=client, menu_id=menu_id, submenu_id=submenu_id
    )
    assert create_dish_response.status_code == 201, create_dish_response.text
    dish_data = create_dish_response.json()
    assert all(
        map(lambda item: item in dish_data, ("id", "title", "description", "price"))
    )
    dish_id = dish_data["id"]
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
