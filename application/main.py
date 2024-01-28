from fastapi import FastAPI


from application.menus.views import router as menu_router
from application.submenus.views import router as submenu_router
from application.dishes.views import router as dishes_router
from application.core.db import Base, engine


app = FastAPI()
app.include_router(menu_router)
app.include_router(submenu_router)
app.include_router(dishes_router)


@app.on_event("startup")
def start_db():
    Base.metadata.create_all(bind=engine)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
