from typing import Sequence, Optional

from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession

from src.files.interfaces import (
    FileRepositoryInterface,
    AllowedFilesForUserRepositoryInterface,
)
from src.files.models import File, AllowedFilesForUser
from src.files.schemas import FileCreateSerializer


class FileRepository(FileRepositoryInterface):
    def __init__(self, db: AsyncSession) -> None:
        self._db = db

    async def create_file(self, file_create: FileCreateSerializer) -> str:
        new_file = File(**file_create.model_dump())
        self._db.add(new_file)
        await self._db.commit()
        await self._db.refresh(new_file)

        return new_file.original_name

    async def delete_file(self, id: int) -> None:
        await self._db.execute(delete(File).filter_by(id=id))
        await self._db.commit()

    async def get_file(self, id: int) -> Optional[File]:
        file = await self._db.execute(select(File).filter_by(id=id))
        return file.scalar_one_or_none()

    async def get_file_for_download(self, id: int) -> Optional[File]:
        file = await self.get_file(id=id)
        if file:
            file.downloaded += 1
            self._db.add(file)
            await self._db.commit()
            await self._db.refresh(file)

        return file

    async def get_all_files(self) -> Sequence[File]:
        result = await self._db.execute(select(File))
        return result.scalars().all()


class AllowedFilesForUserRepository(AllowedFilesForUserRepositoryInterface):
    def __init__(self, db: AsyncSession) -> None:
        self._db = db

    async def create_files_access(
        self, allowed_files: list[AllowedFilesForUser]
    ) -> None:
        self._db.add_all(allowed_files)
        await self._db.commit()

    async def delete_files_access(
        self, file_id: int,
        user_ids: set[int],
    ) -> None:
        if not user_ids:
            return
        query = delete(AllowedFilesForUser).where(
            AllowedFilesForUser.allowed_file_id == file_id,
            AllowedFilesForUser.user_id.in_(user_ids),
        )
        await self._db.execute(query)
        await self._db.commit()

    async def get_users_with_access_to_file(
        self, file_id: int
    ) -> Sequence[int]:
        result = await self._db.execute(
            select(AllowedFilesForUser.user_id).filter_by(
                allowed_file_id=file_id
            )
        )

        return result.scalars().all()
