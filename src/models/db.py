from __future__ import annotations

from functools import lru_cache

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.config.settings import settings


@lru_cache(maxsize=1)
def get_engine():
    return create_engine(settings.database_url, future=True, pool_pre_ping=True)


@lru_cache(maxsize=1)
def get_sessionmaker():
    return sessionmaker(autocommit=False, autoflush=False, bind=get_engine(), future=True)


def get_db():
    SessionLocal = get_sessionmaker()
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

