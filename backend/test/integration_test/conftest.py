import pytest
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
import asyncio
from models.models import Base

TEST_DB_URL = "mysql+aiomysql://root:rootpassword@db:3306/test_data?charset=utf8"

async_engine = create_async_engine(TEST_DB_URL, echo=True)
async_session = sessionmaker(
    autocommit=False, autoflush=False, bind=async_engine, class_=AsyncSession
)

@pytest.fixture(scope='function')
def event_loop():
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()

@pytest.fixture()
async def db_session(event_loop):
    async with async_session() as session:
        try:
            yield session
        finally:
            await session.close()
