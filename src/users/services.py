from src.users.exceptions import (
    UserNotFoundError,
    UserAlreadyExistsError,
)
from src.users.interfaces import UserServiceInterface, UserRepositoryInterface
from src.users.schemas import UserResponseSerializer, UserCreateSerializer


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
