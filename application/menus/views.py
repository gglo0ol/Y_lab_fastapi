from fastapi import APIRouter, Depends, HTTPException
from menus.schemas import MenuCreate, MenuResponse
from menus.service_repository import MenuService
from sqlalchemy.orm.exc import NoResultFound

router = APIRouter(prefix='/api/v1/menus', tags=['Menu'])


@router.post(
    '/', status_code=201, response_model=MenuResponse, summary='Создать новое меню'
)
def create_menu_endpoint(
    data: MenuCreate, repo: MenuService = Depends()
) -> MenuResponse:
    return repo.create_menu(data)


@router.get('/', response_model=list[MenuResponse], summary='Получить список всех меню')
def get_all_menus_endpoint(repo: MenuService = Depends()) -> list[MenuResponse]:
    return repo.get_all_menus()


@router.get(
    '/{menu_id}/',
    response_model=MenuResponse,
    summary='Получить меню',
    responses={404: {'description': 'Menu not found'}},
)
def get_menu_endpoint(menu_id: str, repo: MenuService = Depends()) -> MenuResponse:
    try:
        return repo.get_menu_by_id(menu_id=menu_id)
    except NoResultFound as error:
        raise HTTPException(status_code=404, detail=error.args[0])


@router.get(
    '/counts/{menu_id}/',
    summary='Получить список подмню и блюд для конкретного меню',
    responses={404: {'description': 'Menu not found'}},
)
def get_menu_submenus_and_dishes_count_endpoint(
    menu_id: str, repo: MenuService = Depends()
) -> dict:
    try:
        return repo.get_menu_submenus_and_dishes_count(menu_id=menu_id)
    except NoResultFound as error:
        raise HTTPException(status_code=404, detail=error.args[0])


@router.patch(
    '/{menu_id}/',
    response_model=MenuResponse,
    summary='Обновить меню',
    responses={404: {'description': 'Menu not found'}},
)
def update_menu_endpoint(
    menu_id: str, get_update: MenuCreate, repo: MenuService = Depends()
) -> MenuResponse | dict:
    try:
        return repo.update_menu(menu_id=menu_id, data=get_update)
    except NoResultFound as error:
        raise HTTPException(status_code=404, detail=error.args[0])


@router.delete(
    '/{menu_id}/',
    summary='Удалить меню (при этом удалятся все подменю и блюда данного меню)',
    responses={404: {'description': 'Menu not found'}},
)
def delete_menu_endpoint(menu_id: str, repo: MenuService = Depends()) -> dict:
    try:
        return repo.delete_menu(menu_id=menu_id)
    except NoResultFound as error:
        raise HTTPException(status_code=404, detail=error.args[0])
