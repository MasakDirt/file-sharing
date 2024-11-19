import bcrypt
from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import validates

from src.database.base import Base
from src.users.validators import validate_username, validate_email


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String(300))
    email = Column(String(255), unique=True)
    username = Column(String(255), unique=True)
    _hashed_password = Column("hashed_password", String(255))
    is_staff = Column(Boolean, default=False)
    is_superuser = Column(Boolean, default=False)

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
