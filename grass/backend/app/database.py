import contextlib
from typing import Any, AsyncIterator

from app.config import settings
from sqlalchemy.ext.asyncio import (
    AsyncConnection,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class DatabaseSessionManager:
    # Инициализируем менеджера сессий, принимая хост и дополнительные настройки для движка
    def __init__(self, host: str, engine_kwargs: dict[str, Any] = {}):
        self._engine = create_async_engine(host, **engine_kwargs)
        # Создаем ?фабрику? асинхронных сессий
        self._sessionmaker = async_sessionmaker(autocommit=False, bind=self._engine)

    async def close(self):
        if self._engine is None:
            raise Exception("DatabaseSessionManager is not initialized")
        # Освобождаем ресурсы асинхронного движка
        await self._engine.dispose()
        # Сбрасываем ссылки на движок и фабрику, что бы их скушал сборщик мусора
        self._engine = None
        self._sessionmaker = None

    @contextlib.asynccontextmanager
    async def connect(self) -> AsyncIterator[AsyncConnection]:
        if self._engine is None:
            raise Exception("DatabaseSessionManager is not initialized")
        # Открываем транзакцию на асинхронном подключении к бд. Атомарное? И если не сделать rollback?
        async with self._engine.begin() as connection:
            try:
                yield connection
            except Exception:
                # Откат транзакции в случае ошибки, то есть это атомарная операция
                await connection.rollback()
                raise

    @contextlib.asynccontextmanager
    async def session(self) -> AsyncIterator[AsyncSession]:
        if self._sessionmaker is None:
            raise Exception("DatabaseSessionManager is not initialized")

        session = self._sessionmaker()
        try:
            yield session
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()


sessionmanager = DatabaseSessionManager(settings.database_url, {"echo": settings.echo_sql})


async def get_db_session():
    async with sessionmanager.session() as session:
        yield session
