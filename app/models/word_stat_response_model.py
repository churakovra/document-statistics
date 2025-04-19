from pydantic import BaseModel


class WordStats(BaseModel):
    word: str
    words_in_file_count: int  # Сколько раз слово встречается в файле. Для расчета tf
    file_size: int  # Размер файла. Для расчета tf
    file_count: int  # В скольких файлах встречается слово. Для расчета idf
    files_count: int  # Размер пула файлов. Для расчета idf
    tf: int | float = None
    idf: int | float = None
