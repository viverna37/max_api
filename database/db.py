from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import declarative_base
import os

# Базовый класс для моделей

Base = declarative_base()


class Database:
    def __init__(self):
        self.engine = None
        self.session_factory = None

    async def init(self, database_url: str):
        self.engine = create_async_engine(
            database_url,
            echo=False,
            pool_size=20,
            max_overflow=10,
            pool_pre_ping=True,  # 🔥 обязательно
            pool_recycle=1800,
        )

        self.session_factory = async_sessionmaker(
            self.engine,
            class_=AsyncSession,
            expire_on_commit=False,
            autoflush=False,
        )

    def session(self) -> AsyncSession:
        """Одна сессия — один апдейт"""
        return self.session_factory()

    async def create_tables(self):
        """Создать все таблицы"""
        try:
            async with self.engine.begin() as conn:
                print("✅ Подключение к БД успешно")
                await conn.run_sync(Base.metadata.create_all)
                print("✅ Таблицы созданы/проверены")
        except Exception as e:
            print(f"❌ Ошибка при создании таблиц: {e}")
            raise

    async def close(self):
        """Закрыть подключение"""
        await self.engine.dispose()


# Глобальный экземпляр БД
db = Database()
