from fastapi import APIRouter, Depends
from menus.schemas import MenuCreate, MenuResponse
from menus.service_repository import MenuService

router = APIRouter(prefix='/api/v1/menus', tags=['Menu'])


@router.post('/', status_code=201, response_model=MenuResponse)
def create_menu_endpoint(
    data: MenuCreate, repo: MenuService = Depends()
) -> MenuResponse:
    return repo.create_menu(data)


@router.get('/', response_model=list[MenuResponse])
def get_all_menus_endpoint(repo: MenuService = Depends()) -> list[MenuResponse]:
    return repo.get_all_menus()


@router.get('/{menu_id}/', response_model=MenuResponse)
def get_menu(menu_id: str, repo: MenuService = Depends()) -> MenuResponse:
    return repo.get_menu_by_id(menu_id=menu_id)


@router.get('/counts/{menu_id}/')
def get_menu_submenus_and_dishes_count(
    menu_id: str, repo: MenuService = Depends()
) -> dict:
    return repo.get_menu_submenus_and_dishes_count(menu_id=menu_id)


@router.patch('/{menu_id}/', response_model=MenuResponse)
def update_menu(
    menu_id: str, get_update: MenuCreate, repo: MenuService = Depends()
) -> MenuResponse:
    return repo.update_menu(menu_id=menu_id, data=get_update)


@router.delete('/{menu_id}/')
def delete_menu(menu_id: str, repo: MenuService = Depends()) -> dict:
    return repo.delete_menu(menu_id=menu_id)
