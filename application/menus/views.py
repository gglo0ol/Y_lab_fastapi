from fastapi import Depends, APIRouter, HTTPException, BackgroundTasks
from sqlalchemy.exc import NoResultFound
from typing import Sequence

from application.menus.schemas import MenuCreate, MenuResponse, MenuSubmenuDishes
from application.menus.service_repository import MenuService

router = APIRouter(prefix="/api/v1/menus", tags=["Menu"])


@router.post(
    "/", status_code=201, response_model=MenuResponse, summary="Создать новое меню"
)
async def create_menu_endpoint(
    background_task: BackgroundTasks,
    data: MenuCreate,
    repo: MenuService = Depends(),
) -> MenuResponse:
    return await repo.create_menu(data, background_task=background_task)


@router.get("/", response_model=list[MenuResponse], summary="Получить список всех меню")
async def get_all_menus_endpoint(
    background_task: BackgroundTasks, repo: MenuService = Depends()
) -> list[MenuResponse]:
    return await repo.get_all_menus(background_task=background_task)


@router.get(
    "/{menu_id}/",
    response_model=MenuResponse,
    summary="Получить меню",
    responses={404: {"description": "menu not found"}},
)
async def get_menu_endpoint(
    background_task: BackgroundTasks,
    menu_id: str,
    repo: MenuService = Depends(),
) -> MenuResponse:
    try:
        return await repo.get_menu_by_id(
            menu_id=menu_id, background_task=background_task
        )
    except NoResultFound as error:
        raise HTTPException(status_code=404, detail=error.args[0])


@router.get(
    "/counts/{menu_id}/",
    summary="Получить список подмню и блюд для конкретного меню",
    responses={404: {"description": "menu not found"}},
)
async def get_menu_submenus_and_dishes_count_endpoint(
    menu_id: str, repo: MenuService = Depends()
):
    try:
        return await repo.get_menu_submenus_and_dishes_count(menu_id=menu_id)
    except NoResultFound as error:
        raise HTTPException(status_code=404, detail=error.args[0])


@router.patch(
    "/{menu_id}/",
    response_model=MenuResponse,
    summary="Обновить меню",
    responses={404: {"description": "Menu not found"}},
)
async def update_menu_endpoint(
    background_task: BackgroundTasks,
    menu_id: str,
    get_update: MenuCreate,
    repo: MenuService = Depends(),
) -> MenuResponse | dict:
    try:
        return await repo.update_menu(
            menu_id=menu_id, data=get_update, background_task=background_task
        )
    except NoResultFound as error:
        raise HTTPException(status_code=404, detail=error.args[0])


@router.delete(
    "/{menu_id}/",
    summary="Удалить меню (при этом удалятся все подменю и блюда данного меню)",
    responses={404: {"description": "Menu not found"}},
)
async def delete_menu_endpoint(
    background_task: BackgroundTasks,
    menu_id: str,
    repo: MenuService = Depends(),
) -> dict:
    try:
        return await repo.delete_menu(menu_id=menu_id, background_task=background_task)
    except NoResultFound as error:
        raise HTTPException(status_code=404, detail=error.args[0])


@router.get(
    "tree",
    status_code=200,
    summary="Возвращает полное древо меню (все подменю и блюда)",
    response_model=Sequence[MenuSubmenuDishes],
)
async def menu_submenu_dishes(
    background_task: BackgroundTasks,
    repo: MenuService = Depends(),
) -> Sequence[MenuSubmenuDishes]:
    return await repo.get_all_menu_and_submenu_and_dishes(
        background_task=background_task
    )
