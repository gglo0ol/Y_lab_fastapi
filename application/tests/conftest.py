from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from fastapi.testclient import TestClient

from core.config import POSTGRES_USER, POSTGRES_DB, POSTGRES_PASSWORD, DB_HOST
from core.db import Base, get_db, engine
from core.models.base import Menu, Submenu, Dish
from main import app
import pytest


DATABASE_URL_TEST = f"postgresql+psycopg2://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{DB_HOST}:5432/{POSTGRES_DB}"  # localhost:5555


@pytest.fixture(name="session", scope="function")
def session_fixture():
    test_engine = create_engine(url=DATABASE_URL_TEST)
    TestSession = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)
    session = TestSession()
    try:
        yield session
    finally:
        session.close()


@pytest.fixture(name="client", scope="function")
def client_fixture(session: Session):
    def get_session_override():
        return session

    app.dependency_overrides[get_db] = get_session_override
    client = TestClient(app)

    yield client

    app.dependency_overrides.clear()


@pytest.fixture(autouse=True, scope="function")
def setup_bd():
    Base.metadata.create_all(bind=engine)
    try:
        yield
    finally:
        Base.metadata.drop_all(bind=engine)
