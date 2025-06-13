from math import log
from uuid import UUID


class Statistics:
    def get_tf(self, words: list[str]) -> dict[str, dict[str, float]]:
        if len(words) <= 0:
            raise ValueError("В строке должно быть хотя бы 1 слово")

        word_count = 0
        len_words = len(words)
        res = dict[str, dict[str, float]]()
        for search_word in words:
            for word in words:
                if search_word == word:
                    word_count += 1
            tf = {"tf": word_count / len_words}
            if search_word not in res.keys():
                res[search_word] = tf
            word_count = 0
        return res

    def get_idf(
            self,
            tf: dict[str, dict[str, float]],
            documents: dict[UUID, list[str]]
    ) -> dict[str, dict[str, float]]:
        document_count = 0
        len_documents = len(documents)

        for word, tf_stat in tf.items():
            for document_word_list in documents.values():
                if word in document_word_list:
                    document_count += 1
            tf[word]["idf"] = log(len_documents / document_count)
            document_count = 0
        return tf
