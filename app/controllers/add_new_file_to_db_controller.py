from sqlalchemy.orm import Session

from app.controllers.add_file_words_from_new_file_to_db_controller import add_file_words
from app.models.user_file_model import UserFile
from app.models.user_files_db_model import UserFiles


# Добавляем файл в БД + добавляем слова
def add_new_file_to_db(file: UserFile, session: Session) -> int:
    user_file = UserFiles(
        file_name=file.file_name,
        file_size=file.file_size,
        load_datetime=file.load_datetime,
        user=file.user
    )
    session.add(user_file)
    session.commit()
    session.refresh(user_file)

    for word in file.words:
        add_file_words(user_file, word, session)

    session.commit()
    return user_file.id
