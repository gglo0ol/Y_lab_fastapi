import os
from dotenv import load_dotenv

load_dotenv()


POSTGRES_USER = os.getenv("POSTGRES_USER")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
POSTGRES_DB = os.getenv("POSTGRES_DB")
DB_HOST = os.getenv("DB_HOST")
# DB_HOST = "localhost"
DB_PORT = os.getenv("DB_PORT")

REDIS_HOST = os.getenv("REDIS_HOST")
# REDIS_HOST = "localhost"
REDIS_PORT = os.getenv("REDIS_PORT")
REDIS_URL = f"redis://{REDIS_HOST}:{REDIS_PORT}/0"

RABBITMQ_DEFAULT_USER = os.getenv("RABBITMQ_DEFAULT_USER")
RABBITMQ_DEFAULT_PASS = os.getenv("RABBITMQ_DEFAULT_PASS")
RABBITMQ_DEFAULT_PORT = os.getenv("RABBITMQ_DEFAULT_PORT")
RABBITMQ_HOST = os.getenv("RABBITMQ_HOST")

CELERY_STATUS = os.getenv("CELERY_STATUS").lower() == "true"

# LINK = "http://0.0.0.0:8000/api/v1/menus"
LINK = "http://backend:8000/api/v1/menus/"
MENUS_URL = ""
MENU_URL = "{menu_id}/"
SUBMENUS_URL = "{menu_id}/submenus/"
SUBMENU_URL = "{menu_id}/submenus/{submenu_id}/"
DISHES_URL = "{menu_id}/submenus/{submenu_id}/dishes/"
DISH_URL = "{menu_id}/submenus/{submenu_id}/dishes/{dish_id}/"
TREE_URL = "tree/"

connection_db = f"postgresql+asyncpg://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{DB_HOST}:5432/{POSTGRES_DB}"
