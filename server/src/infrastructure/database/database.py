import logging
from asyncio import current_task
from contextlib import asynccontextmanager

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_scoped_session
from sqlalchemy import orm

from infrastructure.database.entities.base import Base

logger = logging.getLogger(__name__)



class PostgresDatabase:
    def __init__(self, database_url: str) -> None:
        self.__engine = create_async_engine(database_url, echo=False, pool_size=5, max_overflow=10)
        self.__session_factory = async_scoped_session(
            orm.sessionmaker(self.__engine, expire_on_commit=False,
            class_=AsyncSession), scopefunc=current_task)


    def create_database(self) -> None:
        Base.metadata.create_all(self.__engine)

    @asynccontextmanager
    async def session(self) -> AsyncSession:
        session: AsyncSession = self.__session_factory()
        try:
            yield session
        except Exception:
            logger.exception('Postgres Session rollback because of exception')
            await session.rollback()
            raise
        finally:
            await session.close()
