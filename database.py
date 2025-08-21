# database.py
from typing import cast

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import declarative_base, sessionmaker

DATABASE_URL = "sqlite+aiosqlite:///./app.db"
engine = create_async_engine(DATABASE_URL, connect_args={"check_same_thread": False})

async_session = cast(sessionmaker, sessionmaker(engine, expire_on_commit=False, class_=AsyncSession))

Base = declarative_base()
