from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DB_URL: str = f"postgresql://postgres:y_lab@localhost:5432/"    # ПЕРЕДЕЛАТЬ