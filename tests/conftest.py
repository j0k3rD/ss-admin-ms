import sys, os
from typing import Generator
import pytest
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine
from starlette.testclient import TestClient
from datetime import datetime
from asyncpg import create_pool


sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.db.models import User
from src.config.settings import get_settings
from src.main import app

USER_NAME = "testuser"
USER_EMAIL = "agm.moya@alumno.um.edu.ar"
USER_PHONE = "1234567890"
PASSWORD = "testpassword"
ROLE = "admin"

async_engine = create_async_engine(url=get_settings.POSTGRES_URL, echo=True)
SessionTesting = sessionmaker(autoflush=False, bind=async_engine, autocommit=False)


@pytest.fixture(scope="function")
async def db():
    pool = await create_pool(dsn="postgresql://j0k3r:mario2014@localhost/ss_admin")
    conn = await pool.acquire()
    yield conn
    await pool.release(conn)
    await pool.close()


@pytest.fixture(scope="function")
async def test_session() -> Generator:
    async with SessionTesting() as session:
        try:
            yield session
        finally:
            await session.close()


@pytest.fixture(scope="function")
def client(test_session):
    with TestClient(app) as c:
        yield c


@pytest.fixture(scope="function")
def inactive_user(test_session):
    model = User()
    model.name = USER_NAME
    model.email = USER_EMAIL
    model.phone = USER_PHONE
    model.role = ROLE
    model.password = hash(PASSWORD)
    model.updated_at = datetime.now()
    model.is_active = False
    test_session.add(model)
    test_session.commit()
    test_session.refresh(model)
    return model


@pytest.fixture(scope="function")
def user(test_session):
    model = User()
    model.name = USER_NAME
    model.email = USER_EMAIL
    model.password = hash(PASSWORD)
    model.updated_at = datetime.now()
    model.verified_at = datetime.now()
    model.is_active = True
    test_session.add(model)
    test_session.commit()
    test_session.refresh(model)
    return model


@pytest.fixture(scope="function")
def unverified_user(test_session):
    model = User()
    model.name = USER_NAME
    model.email = USER_EMAIL
    model.password = hash(PASSWORD)
    model.updated_at = datetime.now()
    model.is_active = True
    test_session.add(model)
    test_session.commit()
    test_session.refresh(model)
    return model
