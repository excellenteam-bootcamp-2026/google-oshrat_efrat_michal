import unittest

from models.corpus import Corpus
from models.occurrence import Occurrence
from models.sentence import Sentence
from search_logic.autocomplete_service import AutocompleteService
from search_logic.scoring import calculate_score


def make_service(texts: list[str]) -> AutocompleteService:
    sentences = {}
    word_index: dict[str, list[Occurrence]] = {}

    for sentence_id, text in enumerate(texts, start=1):
        normalized = " ".join(text.lower().split())
        sentence = Sentence(
            id=sentence_id,
            text=text,
            normalized_text=normalized,
            tokens=normalized.split(),
            file_path="test.txt",
            line_number=sentence_id,
        )
        sentences[sentence_id] = sentence

        for position, word in enumerate(sentence.tokens):
            word_index.setdefault(word, []).append(
                Occurrence(sentence_id, position)
            )

    return AutocompleteService(Corpus(sentences, word_index))


class SearchLogicTests(unittest.TestCase):
    def test_exact_substring_match(self) -> None:
        results = make_service(["The quick brown fox", "A slow turtle"]).search("quick bro")
        self.assertEqual([result.sentence.text for result in results], ["The quick brown fox"])
        self.assertEqual(results[0].score, 18)
        self.assertEqual(results[0].match_type, "exact")

    def test_one_substitution(self) -> None:
        results = make_service(["The quick brown fox"]).search("the quack")
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].match_type, "substitution")

    def test_missing_character(self) -> None:
        results = make_service(["hello world"]).search("helo world")
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].match_type, "insertion")

    def test_extra_character(self) -> None:
        results = make_service(["hello world"]).search("helllo world")
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].match_type, "deletion")

    def test_only_one_error_is_allowed(self) -> None:
        self.assertEqual(make_service(["hello world"]).search("hxllo worlx"), [])

    def test_top_five_and_deduplication(self) -> None:
        results = make_service([f"hello result {index}" for index in range(8)]).search("hello")
        self.assertEqual(len(results), 5)
        self.assertEqual(len({result.sentence.id for result in results}), 5)

    def test_scoring_rules(self) -> None:
        self.assertEqual(calculate_score(10, "exact"), 20)
        self.assertEqual(calculate_score(10, "substitution", 0), 15)
        self.assertEqual(calculate_score(10, "substitution", 8), 19)
        self.assertEqual(calculate_score(10, "deletion", 0), 10)
        self.assertEqual(calculate_score(10, "insertion", 7), 18)


if __name__ == "__main__":
    unittest.main()
