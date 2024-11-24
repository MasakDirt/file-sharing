from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.session import get_db
from src.files.interfaces import FileRepositoryInterface, FileServiceInterface
from src.files.repositories import FileRepository
from src.files.services import FileService


def get_file_repository(
    db: AsyncSession = Depends(get_db)
) -> FileRepositoryInterface:
    return FileRepository(db=db)


def get_file_service(
    file_repository: FileRepositoryInterface = Depends(get_file_repository)
) -> FileServiceInterface:
    return FileService(file_repository=file_repository)
