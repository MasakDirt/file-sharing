from abc import abstractmethod, ABC

from fastapi import UploadFile

from src.files.models import File
from src.files.schemas import FileCreateSerializer, FileResponseSerializer


class FileRepositoryInterface(ABC):
    @abstractmethod
    async def create_file(self, file_create: FileCreateSerializer) -> str:
        pass

    @abstractmethod
    async def delete_file(self, id: int) -> None:
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
