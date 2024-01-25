from pydantic_settings import BaseSettings
import os
from dotenv import load_dotenv

load_dotenv()

POSTGRES_USER = os.getenv("POSTGRES_USER")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
POSTGRES_DB = os.getenv("POSTGRES_DB")

class Settings(BaseSettings):
    DB_URL: str = "postgresql+psycopg2://y_lab:y_lab_password@localhost:5432/postgres_db"    # ПЕРЕДЕЛАТЬ
    connection_db: str = f"postgresql+psycopg2://{POSTGRES_USER}:{POSTGRES_PASSWORD}@localhost:5432/{POSTGRES_DB}"


settings = Settings()