from dishes.schemas import DishCreate, DishResponse, DishCreateWithId
from dishes.service_repository import DishesService
from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm.exc import NoResultFound

router = APIRouter(
    tags=["Dishes"], prefix="/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes"
)


@router.post(
    "/", status_code=201, response_model=DishResponse, summary="Создать новое блюдо"
)
async def create_dish_endpoint(
    background_task: BackgroundTasks,
    menu_id: str,
    submenu_id: str,
    data_in: DishCreateWithId,
    repo: DishesService = Depends(),
) -> DishResponse:
    return await repo.create_dish(
        menu_id=menu_id,
        submenu_id=submenu_id,
        data=data_in,
        background_task=background_task,
    )


@router.get(
    "/{dish_id}",
    response_model=DishResponse,
    summary="Получить блюдо",
    responses={404: {"description": "Dish not found"}},
)
async def get_dish_endpoint(
    background_task: BackgroundTasks,
    menu_id: str,
    submenu_id: str,
    dish_id: str,
    repo: DishesService = Depends(),
) -> DishResponse:
    try:
        return await repo.get_dish(
            menu_id=menu_id,
            submenu_id=submenu_id,
            dish_id=dish_id,
            background_task=background_task,
        )
    except NoResultFound as error:
        raise HTTPException(status_code=404, detail=error.args[0])


@router.patch(
    "/{dish_id}",
    response_model=DishResponse,
    summary="Обновить блюдо",
    responses={404: {"description": "Dish not found"}},
)
async def update_dish_endpoint(
    background_task: BackgroundTasks,
    menu_id: str,
    submenu_id: str,
    dish_id: str,
    data_in: DishCreate,
    repo: DishesService = Depends(),
) -> DishResponse | dict:
    try:
        return await repo.update_dish(
            menu_id=menu_id,
            submenu_id=submenu_id,
            dish_id=dish_id,
            data=data_in,
            background_task=background_task,
        )
    except NoResultFound as error:
        raise HTTPException(status_code=404, detail=error.args[0])


@router.delete(
    "/{dish_id}",
    summary="Удалить блюдо",
    responses={404: {"description": "Dish not found"}},
)
async def delete_dish_endpoint(
    background_task: BackgroundTasks,
    menu_id: str,
    submenu_id: str,
    dish_id: str,
    repo: DishesService = Depends(),
) -> dict:
    try:
        return await repo.delete_dish(
            menu_id=menu_id,
            submenu_id=submenu_id,
            dish_id=dish_id,
            background_task=background_task,
        )
    except NoResultFound as error:
        raise HTTPException(status_code=404, detail=error.args[0])


@router.get(
    "/",
    response_model=list[DishResponse],
    summary="Получить список всех блюд данного подменю",
)
async def get_all_dishes_endpoint(
    background_task: BackgroundTasks,
    menu_id: str,
    submenu_id: str,
    repo: DishesService = Depends(),
) -> list[DishResponse]:
    return await repo.get_all_dishes(
        menu_id=menu_id, submenu_id=submenu_id, background_task=background_task
    )
