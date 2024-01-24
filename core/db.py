from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
# from core.config import Settings

from uuid import uuid4


DATABASE_URL = "postgresql://postgres:y_lab@localhost:5432/"        # Нужно использовать какое то другое имя БД
Base = declarative_base()
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_uuid():
    return str(uuid4())


Base.metadata.create_all(bind=engine)
