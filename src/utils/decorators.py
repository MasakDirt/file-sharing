from functools import wraps
from typing import Callable, Any

from fastapi import Request, HTTPException
from starlette import status


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
