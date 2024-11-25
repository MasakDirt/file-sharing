import os.path

import aiofiles
from fastapi import UploadFile

from src.database.utils import serialize_obj
from src.files.exceptions import FileNotFoundInSystemError
from src.files.interfaces import (
    FileServiceInterface,
    FileRepositoryInterface,
    AllowedFilesForUserServiceInterface,
    AllowedFilesForUserRepositoryInterface,
)
from src.files.models import AllowedFilesForUser, File
from src.files.schemas import FileCreateSerializer, FileResponseSerializer
from src.files.utils import make_unique_filename
from src.files.validators import validate_file_size
from src.settings import UPLOADED_DIR
from src.users.interfaces import UserRepositoryInterface
from src.users.models import User


class FileService(FileServiceInterface):
    def __init__(self, file_repository: FileRepositoryInterface) -> None:
        self._file_repository = file_repository

    async def process_file_create(self, file: UploadFile) -> str:
        await validate_file_size(file)

        original_filename = file.filename
        unique_name = make_unique_filename(original_filename)
        create_file_path = os.path.join(UPLOADED_DIR, unique_name)

        async with aiofiles.open(create_file_path, "w+b") as out_file:
            while content := await file.read(1024):
                await out_file.write(content)

        return await self._file_repository.create_file(
            FileCreateSerializer(
                original_name=original_filename,
                new_file_name=unique_name
            )
        )

    async def get_all_files(self) -> list[FileResponseSerializer]:
        files = await self._file_repository.get_all_files()
        return [
            FileResponseSerializer(**serialize_obj(file))
            for file in files
        ]

    @staticmethod
    def _check_file_and_get_path(file: File) -> str:
        if file:
            file_path = os.path.join(UPLOADED_DIR, file.new_file_name)

            if not os.path.exists(file_path):
                raise FileNotFoundInSystemError

            return file_path

        raise FileNotFoundInSystemError

    async def remove_file(self, id: int) -> None:
        file = await self._file_repository.get_file(id=id)
        await self._file_repository.delete_file(id=id)
        file_path = self._check_file_and_get_path(file)
        os.remove(file_path)

    async def download_file(self, id: int) -> tuple[str, str]:
        file = await self._file_repository.get_file_for_download(id=id)
        file_path = self._check_file_and_get_path(file)

        return file_path, file.original_name


class AllowedFilesForUserService(AllowedFilesForUserServiceInterface):
    def __init__(
        self, allowed_repository: AllowedFilesForUserRepositoryInterface,
        user_repository: UserRepositoryInterface
    ) -> None:
        self._allowed_repository = allowed_repository
        self._user_repository = user_repository

    async def add_file_access(
        self, file_id: int,
        user_ids: set[int]
    ) -> None:
        allowed_files = [
            AllowedFilesForUser(user_id=user_id, allowed_file_id=file_id)
            for user_id in user_ids
        ]
        await self._allowed_repository.create_files_access(allowed_files)

    async def remove_file_access(
        self, file_id: int,
        user_ids: set[int]
    ) -> None:
        await self._allowed_repository.delete_files_access(file_id, user_ids)

    async def get_users_with_access_to_file(self, file_id: int) -> list[User]:
        users = await self._user_repository.get_all_users(with_admins=False)
        allowed_user_ids = await self._allowed_repository.get_users_with_access_to_file(
            file_id
        )

        for user in users:
            user.has_access = user.id in allowed_user_ids

        return users

    async def update_file_access(
        self, file_id: int,
        selected_user_ids: set[int]
    ) -> None:
        current_user_ids = set(
            await self._allowed_repository.get_users_with_access_to_file(
                file_id
            )
        )

        users_to_add = selected_user_ids - current_user_ids
        users_to_remove = current_user_ids - selected_user_ids

        await self.add_file_access(file_id, users_to_add)
        await self.remove_file_access(file_id, users_to_remove)
