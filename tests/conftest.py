from httpx import AsyncClient
import pytest_asyncio

BASE_URL = "http://127.0.0.1:80"  # Убедись, что приложение запущено


@pytest_asyncio.fixture
async def client():
    async with AsyncClient(base_url=BASE_URL) as ac:
        yield ac


@pytest_asyncio.fixture
async def test_recipe(async_client):
    """Создаёт тестовый рецепт, если нужно."""
    payload = {
        "recipe_name": "Тестовый борщ",
        "ingredients": "Свекла, мясо, капуста",
        "description": "Просто борщ",
        "time_cooking": 60,
    }
    response = await async_client.post("/recipes/", json=payload)
    return response.json()
