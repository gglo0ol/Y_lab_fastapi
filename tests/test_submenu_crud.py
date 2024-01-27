# from tests.conftest import client
#
#
# def test_submenu_all_empty():
#     get_submenu_all = client.get("")
#
#
# def test_submenu():
#     create_menu_response = client.post(
#         "/api/v1/menus/",
#         json={"title": "My menu 1", "description": "My menu description 1"},
#     )
#     assert create_menu_response.status_code == 201, create_menu_response.text
#     data = create_menu_response.json()
#     assert "id" in data
#     menu_id = data["id"]
#     all_menu_response = client.get("/api/v1/menus/")
#     assert all_menu_response.json() == [data]
#     create_submenu_response = client.post(
#         f"/api/v1/menus/{menu_id}",
#         json={"title": "My submenu 1", "description": "My submenu description 1"},
#     )
#     assert create_submenu_response.status_code == 201, create_menu_response.text
#     data = create_menu_response.json()
#     assert "id" in data
#     submenu_id = data["id"]
