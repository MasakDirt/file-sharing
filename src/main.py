from fastapi import FastAPI

from src.users.router import router as users_router


app = FastAPI()


app.include_router(users_router)


@app.get("/")
async def root():
    return {"message": "Hello World"}
