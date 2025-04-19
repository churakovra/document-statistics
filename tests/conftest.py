import pytest
from httpx import AsyncClient
from httpx._transports.asgi import ASGITransport

from app.main import app


@pytest.fixture(scope="function")
async def client():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://localhost:8000") as ac:
        yield ac
