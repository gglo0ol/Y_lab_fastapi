from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from redis.asyncio import from_url
from application.core.config import connection_db, REDIS_URL


Base = declarative_base()
engine = create_async_engine(url=connection_db)
AsyncLocalSession = sessionmaker(
    autoflush=False, autocommit=False, bind=engine, class_=AsyncSession
)


async def get_db():
    async with AsyncLocalSession() as async_session:
        yield async_session


async def init_db():
    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.create_all)


async def get_redis():
    redis = from_url(REDIS_URL)
    async with redis as redis:
        yield redis
