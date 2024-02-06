from uuid import uuid4

from core.config import REDIS_URL, settings
from redis import ConnectionPool, Redis
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

Base = declarative_base()
engine = create_engine(settings.connection_db)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# Dependency to get the database session
def get_db()-> SessionLocal:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_uuid() -> str:
    return str(uuid4())


def create_redis()-> ConnectionPool:
    return ConnectionPool.from_url(REDIS_URL)


pool = create_redis()


def get_redis()-> Redis:
    return Redis(connection_pool=pool)
