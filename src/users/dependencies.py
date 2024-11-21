from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.session import get_db
from src.users.interfaces import (
    UserRepositoryInterface,
    UserServiceInterface,
    SessionRepositoryInterface,
    SessionServiceInterface,
    AuthServiceInterface,
)
from src.users.repositories import UserRepository, SessionRepository
from src.users.services import UserService, AuthService, SessionService


def get_user_repository(
    db: AsyncSession = Depends(get_db)
) -> UserRepositoryInterface:
    return UserRepository(db=db)


def get_user_service(
    user_repository: UserRepositoryInterface = Depends(get_user_repository)
) -> UserServiceInterface:
    return UserService(user_repository=user_repository)


def get_session_repository(
    db: AsyncSession = Depends(get_db)
) -> SessionRepositoryInterface:
    return SessionRepository(db=db)


def get_session_service(
    session_repository: SessionRepositoryInterface = Depends(get_session_repository)
) -> SessionServiceInterface:
    return SessionService(session_repository=session_repository)


def get_auth_service(
    user_repository: UserRepositoryInterface = Depends(get_user_repository),
    session_service: SessionServiceInterface = Depends(get_session_service)
) -> AuthServiceInterface:
    return AuthService(
        user_repository=user_repository,
        session_service=session_service
    )
