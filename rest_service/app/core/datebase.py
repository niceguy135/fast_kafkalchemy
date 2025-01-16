from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from app.core.config import settings


# для синхронной работы
sync_engine = create_engine(
    url=settings.DATABASE_URL_psycopg
)
sync_session_factory = sessionmaker(sync_engine)

# для асинхронной работы
async_engine = create_async_engine(
    url=settings.DATABASE_URL_asyncpg
)
async_session_factory = async_sessionmaker(async_engine)
