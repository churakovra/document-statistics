from sqlalchemy import Engine
from sqlalchemy.orm import Session

from app.models.file_contents_db_model import FileContents


async def add_words(words: list[FileContents], engine: Engine):
    with Session(engine) as session:
        for word in words:
            session.add(word)
        session.commit()
        session.refresh(words)
