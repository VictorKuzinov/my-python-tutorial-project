import pytest


@pytest.mark.asyncio
async def test_get_recipe_by_id(client):
    # создаём рецепт (обязательные поля из RecipeIn)
    response = await client.post(
        "/recipes/",
        json={
            "recipe_name": "Test soup",
            "time_cooking": 30,
            "ingredients": "Water, salt, potatoes",
            "description": "Simple test recipe"
        }
    )
    assert response.status_code == 201
    created_recipe = response.json()

    # получаем по id
    response = await client.get(f"/recipes/{created_recipe['recipe_id']}")
    assert response.status_code == 200
    data = response.json()
    assert data["recipe_name"] == "Test soup"
    assert data["time_cooking"] == 30
    assert "ingredients" in data
    assert "description" in data
