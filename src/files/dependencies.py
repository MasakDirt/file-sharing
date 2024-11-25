from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.session import get_db
from src.files.interfaces import (
    FileRepositoryInterface,
    FileServiceInterface,
    AllowedFilesForUserRepositoryInterface,
    AllowedFilesForUserServiceInterface,
)
from src.files.repositories import (
    FileRepository,
    AllowedFilesForUserRepository,
)
from src.files.services import FileService, AllowedFilesForUserService
from src.users.dependencies import get_user_repository
from src.users.interfaces import UserRepositoryInterface


def get_file_repository(
    db: AsyncSession = Depends(get_db)
) -> FileRepositoryInterface:
    return FileRepository(db=db)


def get_file_service(
    file_repository: FileRepositoryInterface = Depends(get_file_repository)
) -> FileServiceInterface:
    return FileService(file_repository=file_repository)


def get_allowed_files_for_user_repository(
    db: AsyncSession = Depends(get_db)
) -> AllowedFilesForUserRepositoryInterface:
    return AllowedFilesForUserRepository(db=db)


def get_allowed_files_for_user_service(
    allowed_repository: AllowedFilesForUserRepositoryInterface = Depends(
        get_allowed_files_for_user_repository
    ),
    user_repository: UserRepositoryInterface = Depends(get_user_repository)
) -> AllowedFilesForUserServiceInterface:
    return AllowedFilesForUserService(
        allowed_repository=allowed_repository,
        user_repository=user_repository
    )
