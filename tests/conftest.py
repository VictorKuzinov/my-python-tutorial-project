from httpx import ASGITransport, AsyncClient
import pytest_asyncio

from my_python_tutorial_project.main import app


@pytest_asyncio.fixture
async def client():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac
