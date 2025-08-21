# schemes.py
from pydantic import BaseModel, ConfigDict, Field


class BaseRecipe(BaseModel):
    recipe_name: str = Field(..., title="Название блюда")
    time_cooking: int = Field(
        ..., title="Время приготовления (в минутах)", ge=1
    )


class RecipeIn(BaseRecipe):
    ingredients: str = Field(..., title="Список ингредиентов")
    description: str = Field(..., title="Описание")


class RecipeOut(BaseRecipe):
    recipe_id: int = Field(..., title="ID рецепта")
    model_config = ConfigDict(from_attributes=True)
    number_views: int = Field(
        ..., title="Количество просмотров", ge=0
    )


class RecipeDetail(BaseModel):
    recipe_name: str = Field(..., title="Название блюда")
    time_cooking: int = Field(..., title="Время приготовления (в минутах)", ge=1)
    ingredients: str = Field(..., title="Список ингредиентов")
    description: str = Field(..., title="Описание")
    model_config = ConfigDict(from_attributes=True)
