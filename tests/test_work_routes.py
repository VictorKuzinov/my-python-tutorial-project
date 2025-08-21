import pytest_asyncio
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_get_recipe_by_id(client: AsyncClient) -> None:
    """
    Проверка получения рецепта по ID.
    """
    response = await client.get("/recipes/1")
    assert response.status_code == 200
    data = response.json()
    assert "recipe_name" in data
    assert "ingredients" in data
    assert "description" in data
    assert "time_cooking" in data


@pytest.mark.asyncio
async def test_get_all_recipes(client: AsyncClient) -> None:
    """
    Проверка получения всех рецептов.
    """
    response = await client.get("/recipes/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


@pytest.mark.asyncio
async def test_create_recipe(client: AsyncClient) -> None:
    """
    Проверка создания рецепта.
    """
    payload: dict = {
        "recipe_name": "Вареники",
        "time_cooking": 25,
        "ingredients": "Мука, вода, картофель",
        "description": "Вкусное украинское блюдо"
    }

    response = await client.post("/recipes/", json=payload)
    assert response.status_code in (200, 201)
    data = response.json()
    assert data["recipe_name"] == "Вареники"
    assert data["number_views"] == 0  # вместо проверки "что его нет"


@pytest.mark.asyncio
async def test_get_recipe_not_found(client: AsyncClient) -> None:
    """
    Проверка обработки случая, когда рецепт не найден.
    """
    response = await client.get("/recipes/9999")
    assert response.status_code == 404
