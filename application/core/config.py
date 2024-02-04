import os

from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv()

POSTGRES_USER = os.getenv('POSTGRES_USER')
POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD')
POSTGRES_DB = os.getenv('POSTGRES_DB')
DB_HOST = os.getenv('DB_HOST')  # localhost
DB_PORT = os.getenv('DB_PORT')

REDIS_HOST = os.getenv('REDIS_HOST')  # localhost
REDIS_PORT = os.getenv('REDIS_PORT')
REDIS_URL = f"redis://{REDIS_HOST}:{REDIS_PORT}/0"  # noqa

MENUS_URL = '/'
MENU_URL = '/{menu_id}'
SUBMENUS_URL = '/{menu_id}/submenus'
SUBMENU_URL = '/{menu_id}/submenus/{submenu_id}'
DISHES_URL = '/{menu_id}/submenus/{submenu_id}/dishes'
DISH_URL = '/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}'


class Settings(BaseSettings):
    # localhost:5432
    connection_db: str = f"postgresql+psycopg2://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{DB_HOST}:5432/{POSTGRES_DB}"  # noqa


settings = Settings()
