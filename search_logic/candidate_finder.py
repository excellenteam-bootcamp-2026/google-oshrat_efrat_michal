from functools import lru_cache

from models.corpus import Corpus


class CandidateFinder:
    def __init__(self, corpus: Corpus) -> None:
        self._corpus = corpus
        self._vocabulary = tuple(corpus.word_index)

    def find_exact_sentence_ids(
        self,
        query: str
    ) -> set[int]:
        """
        חיפוש מהיר לפי המילים המדויקות שבשאילתה.
        """
        tokens = query.split()

        if not tokens:
            return set()

        sentence_sets: list[set[int]] = []

        for token in tokens:
            occurrences = self._corpus.word_index.get(token)

            if occurrences is None:
                continue

            sentence_sets.append({
                occurrence.sentence_id
                for occurrence in occurrences
            })

        if not sentence_sets:
            return set()

        # משפטים שמשותפים לכל המילים שנמצאו
        return set.intersection(*sentence_sets)

    def find_fuzzy_sentence_ids(
        self,
        query: str
    ) -> set[int]:
        """
        מופעל רק כאשר אין מספיק תוצאות מדויקות.
        """
        tokens = query.split()

        if not tokens:
            return set()

        anchor = max(tokens, key=len)
        matching_words = self._find_similar_words(anchor)

        sentence_ids: set[int] = set()

        for word in matching_words:
            occurrences = self._corpus.word_index[word]

            for occurrence in occurrences:
                sentence_ids.add(occurrence.sentence_id)

        return sentence_ids

    @lru_cache(maxsize=512)
    def _find_similar_words(
        self,
        word_to_find: str
    ) -> tuple[str, ...]:
        return tuple(
            word
            for word in self._vocabulary
            if _is_one_edit_away(word_to_find, word)
        )


def _is_one_edit_away(
    first: str,
    second: str
) -> bool:
    if abs(len(first) - len(second)) > 1:
        return False

    first_index = 0
    second_index = 0
    differences = 0

    while (
        first_index < len(first)
        and second_index < len(second)
    ):
        if first[first_index] == second[second_index]:
            first_index += 1
            second_index += 1
            continue

        differences += 1

        if differences > 1:
            return False

        if len(first) > len(second):
            first_index += 1
        elif len(second) > len(first):
            second_index += 1
        else:
            first_index += 1
            second_index += 1

    if (
        first_index < len(first)
        or second_index < len(second)
    ):
        differences += 1

    return differences <= 1