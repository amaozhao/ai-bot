from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from ..chat.settings import settings

async_engine = create_async_engine(
    settings.DATABASE_URL,
    pool_pre_ping=True,
    echo=settings.DATABASE_ECHO,
)
AsyncSessionLocal = async_sessionmaker(
    bind=async_engine,
    autoflush=False,
    future=True,
    expire_on_commit=False,
)


def session():
    return AsyncSessionLocal
