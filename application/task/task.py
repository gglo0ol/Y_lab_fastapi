import logging

from celery import Celery

from core.config import (
    RABBITMQ_DEFAULT_PASS,
    RABBITMQ_DEFAULT_PORT,
    RABBITMQ_DEFAULT_USER,
    RABBITMQ_HOST,
)

from task.parser import Parser
from task.updater import UpdateBase


celery = Celery(
    "task",
    broker=(
        f"amqp://{RABBITMQ_DEFAULT_USER}:{RABBITMQ_DEFAULT_PASS}@"
        f"{RABBITMQ_HOST}:{RABBITMQ_DEFAULT_PORT}"
    ),
)


@celery.task(
    default_retry_delay=15,
    max_retries=None,
)
def update():
    try:
        parser = Parser()
        data = parser.start_parser()
        updater = UpdateBase(data)
        updater.start_update()
    except Exception as error:
        logging.error(error)
    finally:
        update.retry()


# parser = Parser()
# data = parser.start_parser()
# for menu in data:
#     menu_id = menu["id"]
#     print(menu)
#     for submenu in menu["submenus"]:
#         print(f"\t{submenu}")
#         for dish in submenu["dishes"]:
#             print(f"\t\t{dish}")
#
#
# updater = UpdateBase(data)
# updater.start_update()
