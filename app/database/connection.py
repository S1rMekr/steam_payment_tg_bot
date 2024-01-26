from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.asyncio import create_async_engine

DATABASE_URL = "sqlite+aiosqlite:///./users.db"
engine = create_async_engine(DATABASE_URL, echo=True)
Base = declarative_base()

class User(Base):
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True, index=True)
    login = Column(String, unique=True, index=True)