from typing import Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.files.interfaces import FileRepositoryInterface
from src.files.models import File
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
        pass

    async def get_all_files(self) -> Sequence[File]:
        result = await self._db.execute(select(File))
        return result.scalars().all()
