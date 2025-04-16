from sqlalchemy.orm import Session

from app.models.file_contents_db_model import FileContents


async def add_words(words: list[FileContents], session: Session):
    session.add_all(words)
    session.commit()
