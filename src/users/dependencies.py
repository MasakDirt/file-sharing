from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.session import get_db
from src.users.repositories import UserRepository, SessionRepository
from src.users.services import UserService, AuthService, SessionService


def get_user_repository(
    db: AsyncSession = Depends(get_db)
) -> UserRepository:
    return UserRepository(db=db)


def get_user_service(
    user_repository: UserRepository = Depends(get_user_repository)
) -> UserService:
    return UserService(user_repository=user_repository)


def get_session_repository(
    db: AsyncSession = Depends(get_db)
) -> SessionRepository:
    return SessionRepository(db=db)


def get_session_service(
    session_repository: SessionRepository = Depends(get_session_repository)
) -> SessionService:
    return SessionService(session_repository=session_repository)


def get_auth_service(
    user_repository: UserRepository = Depends(get_user_repository),
    session_service: SessionService = Depends(get_session_service)
) -> AuthService:
    return AuthService(
        user_repository=user_repository,
        session_service=session_service
    )
