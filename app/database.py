from fastapi import FastAPI
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.config.preferences import DATABASE_URL
from app.models.base_db_model import Base

engine = create_engine(url=DATABASE_URL, echo=True)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)


async def init_db(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield


def get_session():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
