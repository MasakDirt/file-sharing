from typing import Optional, Sequence

from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession

from src.users.interfaces import (
    UserRepositoryInterface,
    SessionRepositoryInterface,
)
from src.users.models import User, Session
from src.users.schemas import (
    UserCreateSerializer,
    SessionCreateSerializer,
)


class UserRepository(UserRepositoryInterface):
    def __init__(self, db: AsyncSession) -> None:
        self._db = db

    async def get_all_users(self, with_admins: bool = True) -> Sequence[User]:
        if with_admins:
            result = await self._db.execute(select(User))
        else:
            result = await self._db.execute(
                select(User).filter_by(is_superuser=False)
            )
        return result.scalars().all()

    async def get_user_by_id(self, id: int) -> Optional[User]:
        result = await self._db.execute(select(User).where(User.id == id))
        return result.scalar_one_or_none()

    async def _is_field_exists(
        self, field_name: str,
        field_value: str
    ) -> bool:
        result = await self._db.execute(
            select(User).where(getattr(User, field_name) == field_value)
        )

        return result.scalar_one_or_none() is not None

    async def is_username_exist(self, username: str) -> bool:
        return await self._is_field_exists("username", username)

    async def is_email_exist(self, email: str) -> bool:
        return await self._is_field_exists("email", email)

    async def register_user(
        self, user: UserCreateSerializer
    ) -> User:
        new_user = User(**user.model_dump())
        self._db.add(new_user)
        await self._db.commit()
        await self._db.refresh(new_user)

        return new_user

    async def _get_user_by_email(
        self, email: str
    ) -> Optional[User]:
        result = await self._db.execute(
            select(User).where(User.email == email)
        )
        user = result.scalar_one_or_none()

        return user

    async def authenticate_user(
        self, email: str, password: str
    ) -> Optional[User]:
        user = await self._get_user_by_email(email)

        if user and user.check_password(password):
            return user

        return None


class SessionRepository(SessionRepositoryInterface):
    def __init__(self, db: AsyncSession) -> None:
        self._db = db

    async def create_session(self, session: SessionCreateSerializer) -> str:
        new_session = Session(**session.model_dump())
        self._db.add(new_session)
        await self._db.commit()
        await self._db.refresh(new_session)

        return new_session.token

    async def get_session_by_token(self, token: str) -> Optional[Session]:
        result = await self._db.execute(
            select(Session).where(Session.token == token)
        )

        return result.scalar_one_or_none()

    async def delete_session(self, token: str) -> None:
        await self._db.execute(delete(Session).where(Session.token == token))
        await self._db.commit()
