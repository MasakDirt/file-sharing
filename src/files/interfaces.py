from abc import abstractmethod, ABC
from typing import Optional, Sequence

from fastapi import UploadFile

from src.files.models import File, AllowedFilesForUser
from src.files.schemas import FileCreateSerializer, FileResponseSerializer
from src.users.models import User


class FileRepositoryInterface(ABC):
    @abstractmethod
    async def create_file(self, file_create: FileCreateSerializer) -> str:
        pass

    @abstractmethod
    async def delete_file(self, id: int) -> None:
        pass

    @abstractmethod
    async def get_file(self, id: int) -> Optional[File]:
        pass

    @abstractmethod
    async def get_file_for_download(self, id: int) -> Optional[File]:
        pass

    @abstractmethod
    async def get_all_files(self) -> list[File]:
        pass


class FileServiceInterface(ABC):
    @abstractmethod
    async def process_file_create(self, file: UploadFile) -> str:
        pass

    @abstractmethod
    async def get_all_files(self) -> list[FileResponseSerializer]:
        pass

    @abstractmethod
    async def remove_file(self, id: int) -> None:
        pass

    @abstractmethod
    async def download_file(self, id: int) -> tuple[str, str]:
        pass


class AllowedFilesForUserRepositoryInterface(ABC):
    @abstractmethod
    async def create_files_access(
        self, allowed_files: list[AllowedFilesForUser]
    ) -> None:
        pass

    @abstractmethod
    async def delete_files_access(
        self, file_id: int,
        user_ids: set[int],
    ) -> None:
        pass

    @abstractmethod
    async def get_users_with_access_to_file(
        self, file_id: int
    ) -> Sequence[int]:
        pass


class AllowedFilesForUserServiceInterface(ABC):
    @abstractmethod
    async def add_file_access(
        self, file_id: int,
        user_ids: set[int]
    ) -> None:
        pass

    @abstractmethod
    async def remove_file_access(
        self, file_id: int,
        user_ids: set[int]
    ) -> None:
        pass

    @abstractmethod
    async def get_users_with_access_to_file(self, file_id: int) -> list[User]:
        pass

    @abstractmethod
    async def update_file_access(
        self, file_id: int,
        selected_user_ids: set[int]
    ) -> None:
        pass
