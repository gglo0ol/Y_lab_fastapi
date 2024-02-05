from fastapi import APIRouter, Depends
from submenus.schemas import SubmenuCreate, SubmenuResponse
from submenus.servise_repository import SubmenuService

router = APIRouter(tags=['Submenus'], prefix='/api/v1/menus/{menu_id}/submenus')


@router.post(
    '/',
    status_code=201,
    response_model=SubmenuResponse,
    summary='Создать новое подменю',
)
def create_submenu_endpoint(
    menu_id: str, data_in: SubmenuCreate, repo: SubmenuService = Depends()
) -> SubmenuResponse:
    return repo.create_submenu(
        menu_id=menu_id,
        data=data_in,
    )


@router.get('/{submenu_id}', response_model=SubmenuResponse, summary='Получить подменю')
def get_submenu_endpoint(
    menu_id: str, submenu_id: str, repo: SubmenuService = Depends()
) -> SubmenuResponse:
    return repo.get_submenu_by_id(submenu_id=submenu_id, menu_id=menu_id)


@router.get(
    '/',
    response_model=list[SubmenuResponse],
    summary='Получить список всех подменю для меню',
)
def get_all_submenu_endpoint(
    menu_id: str, repo: SubmenuService = Depends()
) -> list[SubmenuResponse]:
    return repo.get_all_submenu(menu_id=menu_id)


@router.patch(
    '/{submenu_id}', response_model=SubmenuResponse, summary='Обновить подменю'
)
def update_submenu_endpoint(
    menu_id: str,
    submenu_id: str,
    data_in: SubmenuCreate,
    repo: SubmenuService = Depends(),
) -> SubmenuResponse | dict:
    return repo.update_submenu_by_id(
        submenu_id=submenu_id, data=data_in, menu_id=menu_id
    )


@router.delete(
    '/{submenu_id}',
    summary='Удалить подменю (при этом удалятся все блюда этого подменю)',
)
def delete_submenu_endpoint(
    menu_id: str, submenu_id: str, repo: SubmenuService = Depends()
) -> dict:
    return repo.delete_submenu_by_id(submenu_id=submenu_id, menu_id=menu_id)
