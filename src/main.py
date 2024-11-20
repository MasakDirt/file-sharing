from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from src.settings import STATIC_DIR
from src.users.router import router as users_router


app = FastAPI()


app.include_router(users_router)


@app.get("/")
async def root():
    return {"message": "Hello World"}


app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")
