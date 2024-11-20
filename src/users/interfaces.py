from abc import ABC, abstractmethod

from src.users.schemas import UserResponseSerializer, UserCreateSerializer


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
