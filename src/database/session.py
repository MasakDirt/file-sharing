import os

from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker


load_dotenv()


def get_db_url() -> str:
    return (
        f"mysql+aiomysql://{os.getenv('MYSQL_USER')}:{os.getenv('MYSQL_PASSWORD')}"
        f"@{os.getenv('HOST')}:3306/{os.getenv('MYSQL_DATABASE')}"
    )


engine = create_async_engine(
    get_db_url(),
    echo=os.getenv("DEBUG") == "True",
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
