from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from application.core.config import settings

from uuid import uuid4


Base = declarative_base()
engine = create_engine(settings.connection_db)
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
