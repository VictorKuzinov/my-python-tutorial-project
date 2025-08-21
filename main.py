# main.py

# Stdlib
from contextlib import asynccontextmanager
from typing import Annotated, List

# Third party
from fastapi import FastAPI, HTTPException, Path, status
from sqlalchemy import asc, desc, select

# Local
from database import async_session, engine
import models
import schemas


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Контекст жизненного цикла приложения:
    - При старте создаёт таблицы в базе данных.
    - При завершении — закрывает соединение с БД.
    """
    async with engine.begin() as conn:
        await conn.run_sync(models.Base.metadata.create_all)
    yield
    await engine.dispose()


app = FastAPI(lifespan=lifespan)


@app.post(
    "/recipes/", response_model=schemas.RecipeOut, status_code=status.HTTP_201_CREATED
)
async def create_recipe(recipe: schemas.RecipeIn) -> schemas.RecipeOut:
    """
    Создание нового рецепта.
    """
    new_recipe = models.Recipe(**recipe.model_dump())
    async with async_session() as session:
        async with session.begin():
            session.add(new_recipe)
        await session.refresh(new_recipe)
        return new_recipe


@app.get(
    "/recipes/", response_model=List[schemas.RecipeOut], status_code=status.HTTP_200_OK
)
async def get_all_recipes() -> List[schemas.RecipeOut]:
    """
    Получение всех рецептов.
    """
    async with async_session() as session:
        result = await session.execute(
            select(models.Recipe).order_by(
                desc(models.Recipe.number_views),
                asc(models.Recipe.time_cooking),
            )
        )
        recipes = result.scalars().all()
        return recipes


@app.get(
    "/recipes/{recipe_id}",
    response_model=schemas.RecipeDetail,
    status_code=status.HTTP_200_OK,
)
async def get_recipe_id(
    recipe_id: Annotated[int, Path(title="ID рецепта")],
) -> schemas.RecipeDetail:
    """
    Получение рецепта по ID.
    """
    async with async_session() as session:
        result = await session.execute(
            select(models.Recipe).where(models.Recipe.recipe_id == recipe_id)
        )
        recipe = result.scalar_one_or_none()

        if recipe is None:
            raise HTTPException(status_code=404, detail="Рецепт не найден")

        recipe.number_views += 1
        await session.commit()
        await session.refresh(recipe)
        return recipe
