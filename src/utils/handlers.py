import logging

from fastapi import Request, FastAPI, HTTPException
from fastapi_csrf_protect.exceptions import CsrfProtectError

from src.settings import TEMPLATES


logger = logging.getLogger("uvicorn.error")


async def _exception_handler_template(
    request: Request,
    status_code: int,
    detail: str
) -> TEMPLATES.TemplateResponse:
    logger.error(f"Code: {status_code} - {detail}")

    return TEMPLATES.TemplateResponse(
        request=request,
        name="errors/error.html",
        context={
            "detail": detail,
            "status_code": status_code
        }
    )


async def file_exception_handler(
    request: Request,
    exception: HTTPException
) -> TEMPLATES.TemplateResponse:
    return await _exception_handler_template(
        request=request,
        status_code=exception.status_code,
        detail=exception.detail
    )


async def csrf_protect_exception_handler(
    request: Request,
    exception: CsrfProtectError
) -> TEMPLATES.TemplateResponse:
    return await _exception_handler_template(
        request=request,
        status_code=exception.status_code,
        detail=exception.message
    )


def add_exception_handlers_to_app(app: FastAPI) -> None:
    app.exception_handler(HTTPException)(file_exception_handler)
    app.exception_handler(CsrfProtectError)(csrf_protect_exception_handler)
