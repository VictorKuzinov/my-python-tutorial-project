
# Документация API кулинарной книги

## Описание

Это асинхронное API-приложение на FastAPI, реализующее функциональность кулинарной книги. Сервис позволяет:

- Добавлять новые рецепты.
- Получать список всех рецептов с сортировкой по популярности.
- Получать детальную информацию о рецепте по `id`.

---

## Структура проекта

```plaintext
homework/
│
├── main.py             # Основной модуль FastAPI
├── models.py           # SQLAlchemy-модель рецепта
├── schemas.py          # Pydantic-схемы запросов и ответов
├── database.py         # Подключение к БД и создание движка
└── tests/
    └── test_work_routes.py  # Pytest-тесты с AsyncClient
```

---

## Модели базы данных (`models.py`)

```python
class Recipe(Base):
    __tablename__ = 'recipes'
    recipe_id = Column(Integer, primary_key=True, index=True)
    recipe_name = Column(String, index=True)
    number_views = Column(Integer, default=0)
    time_cooking = Column(Integer)
    ingredients = Column(Text)
    description = Column(Text)
```

---

## Pydantic-схемы (`schemas.py`)

```python
class BaseRecipe(BaseModel):
    recipe_name: str
    time_cooking: int

class RecipeIn(BaseRecipe):
    ingredients: str
    description: str

class RecipeOut(BaseRecipe):
    recipe_id: int
    number_views: int

class RecipeDetail(BaseModel):
    recipe_name: str
    time_cooking: int
    ingredients: str
    description: str
```

---

## Основные маршруты (`main.py`)

### POST `/recipes/`

Создание нового рецепта.

**Request Body** (schema: `RecipeIn`):
```json
{
  "recipe_name": "Оливье",
  "time_cooking": 30,
  "ingredients": "Картофель, морковь, яйца",
  "description": "Новогодний салат"
}
```

**Response** (schema: `RecipeIn`)

---

### GET `/recipes/`

Получение списка всех рецептов, отсортированных по:
- убыванию просмотров
- возрастанию времени приготовления

**Response** (schema: `List[RecipeOut]`)

---

### GET `/recipes/{recipe_id}`

Получение детальной информации по ID рецепта и увеличение счётчика просмотров.

**Response** (schema: `RecipeDetail`)

---

## Пример запуска (локально)

```bash
uvicorn main:app --reload --port 8000
```

Swagger-документация: [http://localhost:8000/docs](http://localhost:8000/docs)

---

## Тесты (`test_work_routes.py`)

Написаны 4 асинхронных теста:
- `test_get_recipe_by_id`
- `test_get_all_recipes`
- `test_create_recipe`
- `test_get_recipe_not_found`

Для запуска:

```bash
pytest -v tests/test_work_routes.py
```

---

## Используемые технологии

- **FastAPI** — web-фреймворк.
- **SQLAlchemy 2.0** — ORM для работы с SQLite.
- **Pydantic** — валидация входящих/исходящих данных.
- **httpx.AsyncClient** — асинхронное тестирование.
- **pytest** — тестовый фреймворк.
