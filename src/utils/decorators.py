from functools import wraps
from typing import Callable, Any

from fastapi import Request, HTTPException
from fastapi_csrf_protect import CsrfProtect
from starlette import status

from src.settings import TEMPLATES


def admin_only(func: Callable) -> Callable:
    @wraps(func)
    async def inner(request: Request, *args, **kwargs) -> Any:
        user = request.state.user

        if not user.is_admin():
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Access Denied"
            )

        return await func(request, *args, **kwargs)

    return inner


def set_csrf_token(func: Callable) -> Callable:
    @wraps(func)
    async def inner(
        request: Request,
        csrf_protect: CsrfProtect,
        *args,
        **kwargs
    ) -> TEMPLATES.TemplateResponse:
        csrf_token, signed_token = csrf_protect.generate_csrf_tokens()
        request.state.csrf_token = csrf_token

        response = await func(
            request=request,
            csrf_protect=csrf_protect,
            *args,
            **kwargs
        )

        csrf_protect.set_csrf_cookie(signed_token, response)

        return response

    return inner


def validate_csrf_token(func: Callable) -> Callable:
    @wraps(func)
    async def inner(
        request: Request,
        csrf_protect: CsrfProtect,
        *args,
        **kwargs
    ) -> Any:
        await csrf_protect.validate_csrf(request)

        response = await func(
            request=request,
            csrf_protect=csrf_protect,
            *args,
            **kwargs
        )
        csrf_protect.unset_csrf_cookie(response)

        return response

    return inner
