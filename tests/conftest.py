import pytest
from httpx import AsyncClient

from app.main import app


@pytest.fixture(scope="module")
async def client():
    async with AsyncClient(app=app, base_url="http://localhost:8000") as ac:
        yield ac