from archive_reader.reader import normalize_text
from models.corpus import Corpus
from models.search_result import SearchResult
from search_logic.candidate_finder import CandidateFinder
from search_logic.matching import find_best_match


class AutocompleteService:
    def __init__(self, corpus: Corpus) -> None:
        self._corpus = corpus
        self._candidate_finder = CandidateFinder(corpus)

    def search(
        self,
        user_input: str,
        limit: int = 5
    ) -> list[SearchResult]:

        query = normalize_text(user_input)

        if not query or limit <= 0:
            return []

        # שלב 1: קודם מחפשים רק התאמה מדויקת
        exact_sentence_ids = (
            self._candidate_finder.find_exact_sentence_ids(query)
        )

        exact_results = self._build_results(
            query=query,
            sentence_ids=exact_sentence_ids,
            exact_only=True
        )

        exact_results.sort(key=_result_sort_key)

        # אם כבר מצאנו 5 — לא מפעילים חיפוש שגיאות
        if len(exact_results) >= limit:
            return exact_results[:limit]

        # שלב 2: רק אם חסרות תוצאות מפעילים fuzzy
        fuzzy_sentence_ids = (
            self._candidate_finder.find_fuzzy_sentence_ids(query)
        )

        exact_result_ids = {
            result.sentence.id
            for result in exact_results
        }

        fuzzy_sentence_ids -= exact_result_ids

        fuzzy_results = self._build_results(
            query=query,
            sentence_ids=fuzzy_sentence_ids,
            exact_only=False
        )

        fuzzy_results = [
            result
            for result in fuzzy_results
            if result.match_type != "exact"
        ]

        fuzzy_results.sort(key=_result_sort_key)

        return (
            exact_results + fuzzy_results
        )[:limit]

    def _build_results(
        self,
        query: str,
        sentence_ids: set[int],
        exact_only: bool
    ) -> list[SearchResult]:

        results: list[SearchResult] = []

        for sentence_id in sentence_ids:
            sentence = self._corpus.sentences[sentence_id]

            if exact_only:
                if query not in sentence.normalized_text:
                    continue

                results.append(
                    SearchResult(
                        sentence=sentence,
                        score=len(query) * 2,
                        match_type="exact",
                        error_position=None
                    )
                )

                continue

            match = find_best_match(
                query,
                sentence.normalized_text
            )

            if match is None:
                continue

            results.append(
                SearchResult(
                    sentence=sentence,
                    score=match.score,
                    match_type=match.match_type,
                    error_position=match.error_position
                )
            )

        return results


def _result_sort_key(
    result: SearchResult
) -> tuple[float, str, int]:
    return (
        -result.score,
        result.sentence.normalized_text,
        result.sentence.id
    )