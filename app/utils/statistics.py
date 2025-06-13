from math import log
from uuid import UUID


class Statistics:
    def get_tf(self, words: list[str]) -> dict[str, dict[str, float]]:
        if len(words) <= 0:
            raise ValueError("В строке должно быть хотя бы 1 слово")

        word_count = 0
        len_words = len(words)
        tf = dict[str, dict[str, float]]()
        for search_word in words:
            for word in words:
                if search_word == word:
                    word_count += 1
            tf[search_word] = {"tf": word_count / len_words}
            word_count = 0

        return tf

    def get_idf(
            self,
            words: dict[str, dict[str, float]],
            documents: dict[UUID, list[str]]
    ) -> dict[str, list[dict[str, float]]]:
        document_count = 0
        len_documents = len(documents)
        res = dict[str, list[dict[str, float]]]()

        for uuid, document_words in documents.items():
            for word, tf in words.items():
                if word in document_words:
                    document_count += 1
                idf = float(log(len_documents / document_count + 1))
                idf_res = {"idf": idf}
                res[word] = list()
                res[word].append(tf)
                res[word].append(idf_res)
                document_count = 0
        return res
