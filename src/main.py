from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles

from src.middlewares import authentication_middleware, add_user_to_templates
from src.settings import STATIC_DIR, TEMPLATES
from src.users.router import router as users_router


app = FastAPI()

app.include_router(users_router)

app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

app.middleware("http")(authentication_middleware)
app.middleware("http")(add_user_to_templates)


@app.get("/")
async def root(request: Request) -> TEMPLATES.TemplateResponse:
    return TEMPLATES.TemplateResponse(
        request=request,
        name="index.html"
    )
