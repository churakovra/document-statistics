from math import log
from uuid import UUID

from app.config.preferences import STATISTICS_LENGTH
from app.schemas.statistics.statistics_dto import StatisticsDTO


class StatisticsService:
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

    def sort_statistics(self, statistics: dict[str, dict[str, float]]) -> dict[str, dict[str, float]]:
        response = dict()
        tfs_set = {tf["tf"] for tf in statistics.values()}
        tfs = [tf for tf in tfs_set]
        tfs.sort()
        while len(response) < STATISTICS_LENGTH or len(response) < len(statistics):
            for word, stat in statistics.items():
                if stat["tf"] <= tfs[0]:
                    response[word] = stat
                if len(response) >= STATISTICS_LENGTH or len(response) >= len(statistics):
                    return response
            tfs.remove(tfs[0])
        return response

    def get_statistics_response(self, statistics: list[StatisticsDTO]) -> dict[str, dict[str, float]]:
        response = dict()
        for statistic in statistics:
            word = statistic.word
            tf = statistic.tf
            idf = statistic.idf
            response[word] = {"tf": tf, "idf": idf}
        return response
