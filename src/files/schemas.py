from pydantic import BaseModel


class FileCreateSerializer(BaseModel):
    original_name: str
    new_file_name: str


class FileResponseSerializer(BaseModel):
    id: int
    original_name: str
    downloaded: int
