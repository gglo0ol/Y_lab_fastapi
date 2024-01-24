from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DB_URL: str = "postgresql://postgres:y_lab@localhost:5432/"    # ПЕРЕДЕЛАТЬ


settings = Settings()