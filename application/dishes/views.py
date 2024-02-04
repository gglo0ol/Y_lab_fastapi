from dishes.schemas import DishCreate, DishResponse
from dishes.service_repository import DishesService
from fastapi import APIRouter, Depends

router = APIRouter(
    tags=['Dishes'], prefix='/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes'
)


@router.post('/', status_code=201, response_model=DishResponse)
def create_dish_endpoint(
    menu_id: str, submenu_id: str, data_in: DishCreate, repo: DishesService = Depends()
) -> DishResponse:
    return repo.create_dish(menu_id=menu_id, submenu_id=submenu_id, data=data_in)


@router.get('/{dish_id}', response_model=DishResponse)
def get_dish_endpoint(
    menu_id: str, submenu_id: str, dish_id: str, repo: DishesService = Depends()
) -> DishResponse:
    return repo.get_dish(menu_id=menu_id, submenu_id=submenu_id, dish_id=dish_id)


@router.patch('/{dish_id}', response_model=DishResponse)
def update_dish_endpoint(
    menu_id: str,
    submenu_id: str,
    dish_id: str,
    data_in: DishCreate,
    repo: DishesService = Depends(),
) -> DishResponse | dict:
    return repo.update_dish(
        menu_id=menu_id, submenu_id=submenu_id, dish_id=dish_id, data=data_in
    )


@router.delete('/{dish_id}')
def delete_dish_endpoint(
    menu_id: str, submenu_id: str, dish_id: str, repo: DishesService = Depends()
) -> dict:
    return repo.delete_dish(menu_id=menu_id, submenu_id=submenu_id, dish_id=dish_id)


@router.get('/', response_model=list[DishResponse])
def get_all_dishes_endpoint(
    menu_id: str, submenu_id: str, repo: DishesService = Depends()
):
    return repo.get_all_dishes(menu_id=menu_id, submenu_id=submenu_id)
