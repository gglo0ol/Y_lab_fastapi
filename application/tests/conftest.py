from typing import Callable

import pytest
from core.config import (
    DB_HOST,
    POSTGRES_DB,
    POSTGRES_PASSWORD,
    POSTGRES_USER,
)
from core.db import Base, get_db
from main import app
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
import asyncio
from httpx import AsyncClient


# localhost:5555
DATABASE_URL_TEST = f"postgresql+asyncpg://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{DB_HOST}:5432/{POSTGRES_DB}"  # noqa
test_engine = create_async_engine(url=DATABASE_URL_TEST)
TestAsyncLocalSession = sessionmaker(
    autoflush=False, autocommit=False, bind=test_engine, class_=AsyncSession
)


async def override_db():
    async with TestAsyncLocalSession() as async_session:
        yield async_session


@pytest.fixture(scope="session")
def event_loop(request):
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(autouse=True, scope="function")
async def init_db():
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


@pytest.fixture(scope="session", name="client")
async def client():
    app.dependency_overrides = {get_db: override_db}
    async with AsyncClient(app=app, base_url="http://test") as client:
        yield client


@pytest.fixture
def data_menu_create():
    json_create_menu = {"title": "My menu 1", "description": "My menu description 1"}
    return json_create_menu


@pytest.fixture
def data_menu_update():
    json_update_menu = {
        "title": "My updated menu 1",
        "description": "My updated menu description 1",
    }
    return json_update_menu


@pytest.fixture
def data_submenu_create():
    json_submenu_create = {
        "title": "My submenu 1",
        "description": "My submenu description 1",
    }
    return json_submenu_create


@pytest.fixture
def data_submenu_update():
    json_submenu_update = {
        "title": "My updated submenu 1",
        "description": "My updated submenu description 1",
    }
    return json_submenu_update


@pytest.fixture
def data_dishes_create():
    json_dishes_create = {
        "title": "My dish 1",
        "description": "My dish description 1",
        "price": "12.50",
        "discount": 0,
    }
    return json_dishes_create


@pytest.fixture
def data_dishes_update():
    json_dishes_update = {
        "title": "My updated dish 1",
        "description": "My updated dish description 1",
        "price": "14.50",
        "discount": 0,
    }
    return json_dishes_update


def get_routs() -> dict:
    result = {rout.endpoint.__name__: rout.path for rout in app.routes}
    return result


def reverse(function: Callable, **kwargs) -> str:
    routes = get_routs()
    path = routes[function.__name__]
    return path.format(**kwargs)


@pytest.fixture(scope="module")
def saved_data() -> dict:
    return {}
