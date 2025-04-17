from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.user_words_db_model import UserWords


# Вставляем в user_words слово, если его в сущности еще нет
def add_words(word: UserWords, session: Session) -> UserWords:
    stmt = select(UserWords).where(UserWords.word == word.word)
    result = session.execute(stmt)
    exists = result.scalars().first()
    if exists:
        return exists
    session.add(word)
    session.commit()
    session.refresh(word)
    return word
