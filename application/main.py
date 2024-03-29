from fastapi import FastAPI

from core.db import init_db
from menus.views import router as menu_router
from submenus.views import router as submenu_router
from dishes.views import router as dish_router

from task.task import update
from core.config import CELERY_STATUS


app = FastAPI()
app.include_router(menu_router)
app.include_router(submenu_router)
app.include_router(dish_router)


@app.on_event("startup")
async def start_db():
    await init_db()
    if CELERY_STATUS:
        update.delay()


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
