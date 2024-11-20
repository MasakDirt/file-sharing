from abc import ABC, abstractmethod

from src.users.schemas import (
    UserResponseSerializer,
    UserCreateSerializer,
    SessionCreateSerializer,
    UserLoginSerializer,
)


class UserRepositoryInterface(ABC):
    @abstractmethod
    async def get_all_users(self) -> list[UserResponseSerializer]:
        pass

    @abstractmethod
    async def get_user_by_id(self, id: int) -> UserResponseSerializer | None:
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
    ) -> UserResponseSerializer:
        pass

    @abstractmethod
    async def authenticate_user(
        self, email: str, password: str
    ) -> UserResponseSerializer:
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
    async def delete_session(self, token: str) -> None:
        pass


class SessionServiceInterface(ABC):
    @abstractmethod
    async def make_session(self, user_id: int) -> str:
        pass


class AuthServiceInterface(ABC):
    @abstractmethod
    async def login(self, login_data: UserLoginSerializer) -> str:
        pass
