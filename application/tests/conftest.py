import pytest
from core.config import DB_HOST, POSTGRES_DB, POSTGRES_PASSWORD, POSTGRES_USER
from core.db import Base, engine, get_db
from fastapi.testclient import TestClient
from main import app
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

# localhost:5555
DATABASE_URL_TEST = f"postgresql+psycopg2://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{DB_HOST}:5432/{POSTGRES_DB}"


json_create_menu = {'title': 'My menu 1', 'description': 'My menu description 1'}
json_update_menu = {
    'title': 'My updated menu 1',
    'description': 'My updated menu description 1',
}


@pytest.fixture(autouse=True, scope='function')
def setup_bd():
    Base.metadata.create_all(bind=engine)
    try:
        yield
    finally:
        Base.metadata.drop_all(bind=engine)


@pytest.fixture(name='session', scope='module')
def session_fixture():
    test_engine = create_engine(url=DATABASE_URL_TEST)
    TestSession = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)
    session = TestSession()
    try:
        yield session
    finally:
        session.close()


@pytest.fixture(name='client', scope='module')
def client_fixture(session: Session):
    def get_session_override():
        return session

    app.dependency_overrides[get_db] = get_session_override
    client = TestClient(app)

    yield client

    app.dependency_overrides.clear()


@pytest.fixture(scope='function')
def create_menu(
    client: TestClient,
):
    response = client.post('/api/v1/menus/', json=json_create_menu)
    return response


@pytest.fixture(scope='function')
def get_all_menus(client: TestClient):
    response = client.get('/api/v1/menus/')
    return response
