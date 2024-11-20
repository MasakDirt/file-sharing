from pydantic import BaseModel, EmailStr, field_validator

from src.users.validators import validate_username, validate_password_strength


class UserCreateSerializer(BaseModel):
    email: EmailStr
    username: str
    full_name: str
    password: str

    @field_validator("username")
    @classmethod
    def validate_username_field(cls, username: str) -> str:
        validate_username(username)
        return username

    @field_validator("password")
    @classmethod
    def validate_password_strength_field(cls, password: str) -> str:
        validate_password_strength(password)
        return password


class UserLoginSerializer(BaseModel):
    email: EmailStr
    password: str


class UserResponseSerializer(BaseModel):
    id: int
    email: EmailStr
    username: str
    full_name: str
    is_staff: bool
    is_superuser: bool
