from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.utils import serialize_obj
from src.users.interfaces import UserRepositoryInterface
from src.users.models import User
from src.users.schemas import UserResponseSerializer, UserCreateSerializer


class UserRepository(UserRepositoryInterface):
    def __init__(self, db: AsyncSession) -> None:
        self._db = db

    async def get_all_users(self) -> list[UserResponseSerializer]:
        result = await self._db.execute(select(User))
        users = result.scalars().all()
        return [UserResponseSerializer(**serialize_obj(user)) for user in users]

    async def get_user_by_id(self, id: int) -> UserResponseSerializer | None:
        result = await self._db.execute(select(User).where(User.id == id))
        user = result.scalar_one_or_none()
        return UserResponseSerializer(**serialize_obj(user)) if user else None

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
    ) -> UserResponseSerializer:
        new_user = User(**user.model_dump())
        self._db.add(new_user)
        await self._db.commit()
        await self._db.refresh(new_user)
        return UserResponseSerializer(**serialize_obj(new_user))
