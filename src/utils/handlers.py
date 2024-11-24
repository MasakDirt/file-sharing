from fastapi import Request, FastAPI, HTTPException

from src.settings import TEMPLATES


async def file_exception_handler(
    request: Request,
    exception: HTTPException
) -> TEMPLATES.TemplateResponse:
    return TEMPLATES.TemplateResponse(
        request=request,
        name="errors/error.html",
        context={
            "detail": exception.detail,
            "status_code": exception.status_code
        }
    )


def add_exception_handlers_to_app(app: FastAPI) -> None:
    app.exception_handler(HTTPException)(file_exception_handler)
