from fastapi import FastAPI, HTTPException, Depends

from application.core.db import init_db
from application.menus.views import router as menu_router
from application.submenus.views import router as submenu_router
from application.dishes.views import router as dish_router


app = FastAPI()
app.include_router(menu_router)
app.include_router(submenu_router)
app.include_router(dish_router)


@app.on_event("startup")
async def start_db():
    await init_db()


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
