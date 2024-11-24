import os

from fastapi import UploadFile

from src.settings import ALLOWED_EXTENSIONS, MAX_FILE_SIZE


def validate_file_extension(filename: str) -> None:
    file_extension = os.path.splitext(filename)[-1]
    if file_extension not in ALLOWED_EXTENSIONS:
        raise ValueError(f"{file_extension} - invalid file extension")


async def validate_file_size(file: UploadFile) -> None:
    if file.size > MAX_FILE_SIZE:
        raise ValueError(
            f"The maximum size of file must be - "
            f"{(MAX_FILE_SIZE / 1024) / 1024} MB, but your size is "
            f"{round((file.size / 1024) / 1024, 2)} MB"
        )
