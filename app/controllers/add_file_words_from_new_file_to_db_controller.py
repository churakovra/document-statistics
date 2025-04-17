from sqlalchemy.orm import Session

from app.controllers.add_words_from_new_file_to_db_controller import add_words
from app.models.user_files_db_model import UserFiles
from app.models.user_words_db_model import UserWords
from app.models.words_in_file_db_model import FileWords


# Добавляем в file_words слово + файл
def add_file_words(user_file: UserFiles, word: str, session: Session):
    user_word = add_words(UserWords(word=word), session)

    file_word = FileWords(
        id_file=user_file.id,
        id_word=user_word.id
    )
    session.add(file_word)
    session.commit()
    session.refresh(file_word)
