from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship, validates

from src.database.base import Base
from src.files.validators import validate_file_extension


class File(Base):
    __tablename__ = "files"

    id = Column(Integer, primary_key=True, index=True)
    original_name = Column(String(255))
    new_file_name = Column(String(122))
    downloaded = Column(Integer, default=0)

    allowed_for = relationship("AllowedFilesForUser", back_populates="files")

    def __str__(self) -> str:
        return self.original_name

    @validates("original_name")
    def validate_original_name(self, key, original_name: str) -> str:
        validate_file_extension(original_name)
        return original_name


class AllowedFilesForUser(Base):
    __tablename__ = "allowed_user_files"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(
        Integer,
        ForeignKey(
            "users.id",
            ondelete="CASCADE"
        )
    )
    allowed_file_id = Column(
        Integer,
        ForeignKey(
            "files.id",
            ondelete="CASCADE"
        )
    )

    users = relationship("User", back_populates="allowed_files")
    files = relationship("File", back_populates="allowed_for")
