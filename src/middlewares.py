from typing import Optional

from fastapi import Request
from sqlalchemy import select
from starlette.responses import RedirectResponse

from src.database.session import SessionLocal
from src.settings import TEMPLATES
from src.users.models import Session, User


async def authentication_middleware(request: Request, call_next):
    token = request.cookies.get("session")

    async with SessionLocal() as db:
        result = await db.execute(
            select(Session).where(Session.token == token)
        )
        session = result.scalar_one_or_none()

        if session is None or session.is_expired():
            if (
                request.url.path not in ("/login/", "/register/")
                and not request.url.path.startswith("/static/")
            ):
                return RedirectResponse(url="/login/")
        else:
            user_result = await db.execute(
                select(User).filter_by(id=session.user_id)
            )
            request.state.user = user_result.scalar_one_or_none()

    response = await call_next(request)
    return response


async def add_user_to_templates(request: Request, call_next):
    def get_user() -> Optional[User]:
        return getattr(request.state, "user", None)

    TEMPLATES.env.globals["get_user"] = get_user

    response = await call_next(request)
    return response
