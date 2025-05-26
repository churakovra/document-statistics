from sqlalchemy import select, func
from sqlalchemy.orm import Session

from app.models.user_file_model import UserFile
from app.models.user_files_db_model import UserFiles
from app.models.user_words_db_model import UserWords
from app.models.words_in_file_db_model import FileWords


class FileRepository:
    @staticmethod
    # Добавляем файл в БД + добавляем слова
    def add_file(file: UserFile, session: Session) -> int:
        user_file = UserFiles(
            file_name=file.file_name,
            file_size=file.file_size,
            load_datetime=file.load_datetime,
            user=file.user
        )
        session.add(user_file)
        session.commit()
        session.refresh(user_file)

        FileRepository.add_file_words(user_file.id, file, session)

        session.commit()
        return user_file.id

    @staticmethod
    # Добавляем в file_words слово + файл
    def add_file_words(user_file_id: int, file: UserFile, session: Session):
        for word in file.words:
            user_word = FileRepository.add_word(UserWords(word=word), session)

            file_word = FileWords(
                id_file=user_file_id,
                id_word=user_word.id
            )
            session.add(file_word)
            session.commit()
            session.refresh(file_word)

    @staticmethod
    def add_word(word: UserWords, session: Session) -> UserWords:
        stmt = select(UserWords).where(UserWords.word == word.word)
        result = session.execute(stmt)
        exists = result.scalars().first()
        if exists:
            return exists
        session.add(word)
        session.commit()
        session.refresh(word)
        return word

    @staticmethod
    def get_words(file_id: int, session: Session):
        return session.execute(
            select(
                UserWords.word,
                func.count(FileWords.id_word)
            )
            .join(UserWords, FileWords.id_word == UserWords.id)
            .where(FileWords.id_file == file_id)
            .group_by(FileWords.id_word, UserWords.word)
            .order_by(FileWords.id_word.desc())
        ).all()

    @staticmethod
    def get_word_in_files(file_id: int, session: Session):
        return session.execute(
            select(
                func.count(FileWords.id_file.distinct())
            )
            .where(
                FileWords.id_word.in_(
                    select(
                        FileWords.id_word
                    )
                    .where(FileWords.id_file == file_id)
                )
            )
            .group_by(FileWords.id_word)
            .order_by(FileWords.id_word.desc())
        ).all()

    @staticmethod
    def get_file_size(file_id: int, session: Session) -> int:
        return session.scalar(
            select(
                UserFiles.file_size
            )
            .where(UserFiles.id == file_id)
            .group_by(UserFiles.file_size)
        )

    @staticmethod
    def get_files_count(file_id: int, session: Session) -> int:
        return session.scalar(
            select(
                func.count(UserFiles.id)
            )
            .where(UserFiles.id == file_id)
        )
