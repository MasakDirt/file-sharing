from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from src import settings


def get_db_url() -> str:
    return settings.DATABASE_URL


engine = create_async_engine(
    get_db_url(),
    echo=settings.DEBUG,
    future=True,
)

SessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autoflush=False,
    autocommit=False
)


async def get_db() -> AsyncSession:
    async with SessionLocal() as session:
        yield session
