# model.py

from sqlalchemy import Column, String, Integer, Text

from database import Base


class Recipe(Base):
    """
    Модель рецепта в базе данных.
    """
    __tablename__ = 'recipes'

    recipe_id = Column(Integer, primary_key=True, index=True)
    recipe_name = Column(String, index=True)
    number_views = Column(Integer, default=0)
    time_cooking = Column(Integer)
    ingredients = Column(Text)
    description = Column(Text)
