import secrets
from datetime import datetime, timedelta, UTC

from src.database.utils import serialize_obj
from src.users.exceptions import (
    UserNotFoundError,
    UserAlreadyExistsError,
    InvalidCredentialsError,
)
from src.users.interfaces import (
    UserServiceInterface,
    UserRepositoryInterface,
    SessionServiceInterface,
    SessionRepositoryInterface,
    AuthServiceInterface,
)
from src.users.schemas import (
    UserResponseSerializer,
    UserCreateSerializer,
    SessionCreateSerializer,
    UserLoginSerializer,
)


class UserService(UserServiceInterface):
    def __init__(self, user_repository: UserRepositoryInterface) -> None:
        self._user_repository = user_repository

    async def get_all(self) -> list[UserResponseSerializer]:
        users = await self._user_repository.get_all_users()
        return [
            UserResponseSerializer(**serialize_obj(user))
            for user in users
        ]

    async def get_user(self, id: int) -> UserResponseSerializer:
        user = UserResponseSerializer(
            **serialize_obj(
                await self._user_repository.get_user_by_id(id=id)
            )
        )
        if user:
            return user

        raise UserNotFoundError(f"User with id: {id} not found")

    async def create_user(
        self, user: UserCreateSerializer
    ) -> UserResponseSerializer:
        if await self._user_repository.is_username_exist(user.username):
            raise UserAlreadyExistsError(
                f"User with username '{user.username}' already exist!"
            )
        if await self._user_repository.is_email_exist(user.email):
            raise UserAlreadyExistsError(
                f"User with email '{user.email}' already exist!"
            )

        new_user = await self._user_repository.register_user(user)
        return UserResponseSerializer(**serialize_obj(new_user))


class SessionService(SessionServiceInterface):
    def __init__(self, session_repository: SessionRepositoryInterface):
        self._session_repository = session_repository

    @staticmethod
    def _generate_session_token() -> str:
        return secrets.token_urlsafe(32)

    async def make_session(self, user_id: int, remember_me: bool) -> str:
        expired_at = datetime.now(UTC) + timedelta(
            days=10 if remember_me else 3
        )
        session_create_serializer = SessionCreateSerializer(
            token=self._generate_session_token(),
            expired_at=expired_at,
            user_id=user_id
        )
        return await self._session_repository.create_session(
            session_create_serializer
        )

    async def remove_session(self, token: str) -> None:
        await self._session_repository.delete_session(token)


class AuthService(AuthServiceInterface):
    def __init__(
        self, session_service: SessionServiceInterface,
        user_repository: UserRepositoryInterface
    ) -> None:
        self._session_service = session_service
        self._user_repository = user_repository

    async def login(
        self, login_data: UserLoginSerializer,
        remember_me: bool
    ) -> str:
        user = await self._user_repository.authenticate_user(
            email=login_data.email,
            password=login_data.password
        )

        if not user:
            raise InvalidCredentialsError

        token = await self._session_service.make_session(
            user_id=user.id,
            remember_me=remember_me
        )

        return token

    async def logout(self, token: str) -> None:
        await self._session_service.remove_session(token)
