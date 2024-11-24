import os.path

import aiofiles
from fastapi import UploadFile

from src.database.utils import serialize_obj
from src.files.interfaces import FileServiceInterface, FileRepositoryInterface
from src.files.schemas import FileCreateSerializer, FileResponseSerializer
from src.files.utils import make_unique_filename
from src.files.validators import validate_file_size
from src.settings import UPLOADED_DIR


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
