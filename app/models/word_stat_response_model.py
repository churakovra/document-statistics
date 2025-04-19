from pydantic import BaseModel


class WordStats(BaseModel):
    word: str
    words_in_file_count: int  # Сколько раз слово встречается в файле. Для расчета tf
    file_size: int  # Размер файла. Для расчета tf
    file_count: int  # В скольких файлах встречается слово. Для расчета idf
    files_count: int  # Размер пула файлов. Для расчета idf
    tf: int | float = None
    idf: int | float = None

    def __lt__(self, other):
        if not isinstance(other, WordStats):
            return NotImplemented
        return self.idf < other.idf

    def __eq__(self, other):
        if not isinstance(other, WordStats):
            return NotImplemented
        return self.word == other.word and self.tf == other.tf and self.idf == other.idf
