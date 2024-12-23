from abc import ABC, abstractmethod
from typing import Optional

from src.users.models import Session, User
from src.users.schemas import (
    UserResponseSerializer,
    UserCreateSerializer,
    SessionCreateSerializer,
    UserLoginSerializer,
)


class UserRepositoryInterface(ABC):
    @abstractmethod
    async def get_all_users(self, with_admins: bool = True) -> list[User]:
        pass

    @abstractmethod
    async def get_user_by_id(
        self, id: int
    ) -> Optional[User]:
        pass

    @abstractmethod
    async def is_username_exist(self, username: str) -> bool:
        pass

    @abstractmethod
    async def is_email_exist(self, email: str) -> bool:
        pass

    @abstractmethod
    async def register_user(
        self, user: UserCreateSerializer
    ) -> User:
        pass

    @abstractmethod
    async def authenticate_user(
        self, email: str, password: str
    ) -> User:
        pass


class UserServiceInterface(ABC):
    @abstractmethod
    async def get_all(self) -> list[UserResponseSerializer]:
        pass

    @abstractmethod
    async def get_user(self, id: int) -> UserResponseSerializer:
        pass

    @abstractmethod
    async def create_user(
        self, user: UserCreateSerializer
    ) -> UserResponseSerializer:
        pass


class SessionRepositoryInterface(ABC):
    @abstractmethod
    async def create_session(self, session: SessionCreateSerializer) -> str:
        pass

    @abstractmethod
    async def get_session_by_token(self, token: str) -> Optional[Session]:
        pass

    @abstractmethod
    async def delete_session(self, token: str) -> None:
        pass


class SessionServiceInterface(ABC):
    @abstractmethod
    async def make_session(self, user_id: int, remember_me: bool) -> str:
        pass

    @abstractmethod
    async def remove_session(self, token: str) -> None:
        pass


class AuthServiceInterface(ABC):
    @abstractmethod
    async def login(
        self, login_data: UserLoginSerializer,
        remember_me: bool
    ) -> str:
        pass

    @abstractmethod
    async def logout(self, token: str) -> None:
        pass
