from typing import Callable

import pytest
from core.config import DB_HOST, POSTGRES_DB, POSTGRES_PASSWORD, POSTGRES_USER
from core.db import Base, engine, get_db
from fastapi.testclient import TestClient
from main import app
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

# localhost:5555
DATABASE_URL_TEST = f"postgresql+psycopg2://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{DB_HOST}:5432/{POSTGRES_DB}"  # noqa
test_engine = create_engine(url=DATABASE_URL_TEST)
Base.metadata.bind = test_engine


@pytest.fixture(name="session", scope="session")
def session_fixture():
    # test_engine = create_engine(url=DATABASE_URL_TEST)
    TestSession = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)
    session = TestSession()
    # Base.metadata.drop_all(bind=test_engine)
    # Base.metadata.create_all(bind=test_engine)
    try:
        yield session
    finally:
        session.close()


@pytest.fixture(name="client", scope="session")
def client_fixture(session: Session):
    def get_session_override():
        return session

    app.dependency_overrides[get_db] = get_session_override
    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()


@pytest.fixture(scope="session", autouse=True)
def setup_bd():
    Base.metadata.create_all(bind=test_engine)
    try:
        yield
    finally:
        Base.metadata.clear()


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
    }
    return json_dishes_create


@pytest.fixture
def data_dishes_update():
    json_dishes_update = {
        "title": "My updated dish 1",
        "description": "My updated dish description 1",
        "price": "14.50",
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
