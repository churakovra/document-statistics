from contextlib import asynccontextmanager

from fastapi import FastAPI
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.config.preferences import DATABASE_URL
from app.db.models.base import Base

engine = create_engine(url=DATABASE_URL, echo=True)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

@asynccontextmanager
async def init_db(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield


def get_session():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
