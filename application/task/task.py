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
