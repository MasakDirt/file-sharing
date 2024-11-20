import secrets
from datetime import datetime, timedelta

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
        return await self._user_repository.get_all_users()

    async def get_user(self, id: int) -> UserResponseSerializer:
        user = await self._user_repository.get_user_by_id(id=id)
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
        return new_user


class SessionService(SessionServiceInterface):
    def __init__(self, session_repository: SessionRepositoryInterface):
        self._session_repository = session_repository

    @staticmethod
    def _generate_session_token() -> str:
        return secrets.token_urlsafe(32)

    async def make_session(self, user_id: int) -> str:
        session_create_serializer = SessionCreateSerializer(
            token=self._generate_session_token(),
            expired_at=datetime.now() + timedelta(days=1),
            user_id=user_id
        )
        return await self._session_repository.create_session(
            session_create_serializer
        )


class AuthService(AuthServiceInterface):
    def __init__(
        self, session_service: SessionServiceInterface,
        user_repository: UserRepositoryInterface
    ) -> None:
        self._session_service = session_service
        self._user_repository = user_repository

    async def login(self, login_data: UserLoginSerializer) -> str:
        user = await self._user_repository.authenticate_user(
            email=login_data.email,
            password=login_data.password
        )

        if not user:
            raise InvalidCredentialsError

        token = await self._session_service.make_session(user_id=user.id)

        return token
