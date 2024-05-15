from sqlalchemy.ext.asyncio import create_async_engine
from src.config.settings import get_settings
from sqlmodel import SQLModel
from sqlalchemy.orm import sessionmaker
from sqlmodel.ext.asyncio.session import AsyncSession

async_engine = create_async_engine(url=get_settings.POSTGRES_URL, echo=True)


async def init_db():
    async with async_engine.begin() as conn:
        from src.db.models import (
            User,
            Property,
            Service,
            ScrappedData,
            Roles,
            Token,
            ProviderClient,
        )

        await conn.run_sync(SQLModel.metadata.create_all)


async def get_session():
    async_session = sessionmaker(
        bind=async_engine,
        class_=AsyncSession,
        expire_on_commit=False,
    )
    async with async_session() as session:
        yield session
