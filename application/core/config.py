from pydantic_settings import BaseSettings
import os
from dotenv import load_dotenv

load_dotenv()

POSTGRES_USER = os.getenv("POSTGRES_USER")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
POSTGRES_DB = os.getenv("POSTGRES_DB")


class Settings(BaseSettings):
    connection_db: str = f"postgresql+psycopg2://{POSTGRES_USER}:{POSTGRES_PASSWORD}@database/{POSTGRES_DB}"  # localhost:5432


settings = Settings()
