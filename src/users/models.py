import datetime

import bcrypt
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import validates, relationship

from src.database.base import Base
from src.users.validators import validate_username, validate_email


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String(300))
    email = Column(String(255), unique=True)
    username = Column(String(255), unique=True, index=True)
    _hashed_password = Column("hashed_password", String(255))
    is_staff = Column(Boolean, default=False)
    is_superuser = Column(Boolean, default=False)

    sessions = relationship(
        "Session",
        back_populates="user",
        cascade="all, delete-orphan"
    )

    def __str__(self) -> str:
        return f"User {self.username} with email: {self.email}"

    @property
    def password(self) -> None:
        raise AttributeError("Password is not readable attribute")

    @password.setter
    def password(self, password: str) -> None:
        hashed_password = bcrypt.hashpw(
            password.encode("utf-8"),
            bcrypt.gensalt()
        )
        self._hashed_password = hashed_password.decode("utf-8")

    def check_password(self, password: str) -> bool:
        return bcrypt.checkpw(
            password.encode("utf-8"),
            self._hashed_password.encode("utf-8")
        )

    @validates("username")
    def validate_username(self, key, username: str) -> str:
        print(key)
        validate_username(username)
        return username

    @validates("email")
    def validate_email(self, key, email: str) -> str:
        print(key)
        validate_email(email)
        return email


class Session(Base):
    __tablename__ = "sessions"

    id = Column(Integer, primary_key=True, index=True)
    token = Column(String(128), unique=True, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    expired_at = Column(DateTime, nullable=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))

    user = relationship("User", back_populates="sessions")

    def __str__(self):
        return f"Token: {self.token} expire at: {self.expired_at}"

    def is_expired(self):
        return datetime.datetime.now() > self.expired_at
