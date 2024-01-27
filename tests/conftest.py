from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient

from core.config import POSTGRES_USER, POSTGRES_DB, POSTGRES_PASSWORD
from core.db import Base, get_db
from main import app


DATABASE_URL_TEST = f"postgresql+psycopg2://{POSTGRES_USER}:{POSTGRES_PASSWORD}@localhost:5555/{POSTGRES_DB}"  # localhost:5555

test_engine = create_engine(url=DATABASE_URL_TEST)
Test_session = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)

Base.metadata.create_all(bind=test_engine)


def test_get_db():
    test_db = Test_session()
    try:
        yield test_db
    finally:
        test_db.close()


app.dependency_overrides[get_db] = test_get_db

client = TestClient(app)
