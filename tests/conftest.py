import sys, os
import asyncio
from typing import Generator
import pytest
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine
from starlette.testclient import TestClient


sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.db.main import get_session, init_db
from src.config.settings import get_settings
from src.main import app

USER_NAME = "testuser"
USER_EMAIL = "testemail@example.com"
USER_PHONE = "1234567890"
PASSWORD = "testpassword"
ROLE = "admin"

async_engine = create_async_engine(url=get_settings.POSTGRES_URL, echo=True)
SessionTesting = sessionmaker(autoflush=False, bind=async_engine, autocommit=False)


@pytest.fixture(scope="function")
async def test_session() -> Generator:
    async with SessionTesting() as session:
        try:
            yield session
        finally:
            await session.close()


@pytest.fixture(scope="function")
def app_test():
    asyncio.run(init_db())
    yield app


@pytest.fixture
def client():
    with TestClient(app) as c:
        yield c
