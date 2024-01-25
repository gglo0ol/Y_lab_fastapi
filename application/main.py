from fastapi import FastAPI


from menus.views import router as menu_router
from submenus.views import router as submenu_router
from dishes.views import router as dishes_router
from core.db import Base, engine


app = FastAPI()
app.include_router(menu_router)
app.include_router(submenu_router)
app.include_router(dishes_router)

@app.on_event("startup")
def start_db():
    Base.metadata.create_all(bind=engine)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000)
