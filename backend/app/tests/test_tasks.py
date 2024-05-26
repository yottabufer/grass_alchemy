from fastapi.testclient import TestClient
from app.main import app
import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

from app.database import Base, get_db_session

client = TestClient(app)


@pytest.fixture
def anyio_backend():
    return 'asyncio'


def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello World"}


@pytest.mark.anyio
async def test_root():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello World"}


SQLALCHEMY_DATABASE_URL = "postgresql+asyncpg://dev-user:password@postgres:5432/dev_db"

async_engine = create_async_engine(SQLALCHEMY_DATABASE_URL, future=True, echo=True)

TestingSessionLocal = async_sessionmaker(
    bind=async_engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False
)


async def override_get_db():
    async with TestingSessionLocal() as session:
        yield session


app.dependency_overrides[get_db_session] = override_get_db

available_body = {
    'title': 'Write Code',
    'completed': False,
}


@pytest.mark.anyio
async def test_create_task():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post("/api/tasks/create", json=available_body)
    assert response.status_code == 200
    assert response.json()['detail'] == "The title cannot be empty"
