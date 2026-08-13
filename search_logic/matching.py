from dataclasses import dataclass

from search_logic.scoring import (
    DELETION,
    EXACT,
    INSERTION,
    SUBSTITUTION,
    calculate_score,
)


@dataclass(frozen=True, slots=True)
class Match:
    score: int
    match_type: str
    error_position: int | None = None


def find_best_match(query: str, sentence_text: str) -> Match | None:
    """Find an exact substring or a substring obtainable with one edit."""
    if query in sentence_text:
        return Match(calculate_score(len(query), EXACT), EXACT)

    best: Match | None = None

    # The user typed one wrong character.
    for position in range(len(query)):
        before = query[:position]
        after = query[position + 1:]
        start = 0

        while True:
            start = sentence_text.find(before, start)
            if start == -1:
                break

            changed_position = start + position
            after_start = changed_position + 1

            if (
                changed_position < len(sentence_text)
                and sentence_text[changed_position] != query[position]
                and sentence_text.startswith(after, after_start)
            ):
                best = _better(
                    best,
                    Match(
                        calculate_score(len(query), SUBSTITUTION, position),
                        SUBSTITUTION,
                        position,
                    ),
                )
                break

            start += 1

    # Delete one extra character from the user's input.
    for position in range(len(query)):
        variation = query[:position] + query[position + 1:]

        if variation and variation in sentence_text:
            best = _better(
                best,
                Match(
                    calculate_score(len(query), DELETION, position),
                    DELETION,
                    position,
                ),
            )

    # Insert one missing character into the user's input.
    for position in range(len(query) + 1):
        before = query[:position]
        after = query[position:]
        start = 0

        while True:
            start = sentence_text.find(before, start)
            if start == -1:
                break

            inserted_position = start + position

            if (
                inserted_position < len(sentence_text)
                and sentence_text.startswith(after, inserted_position + 1)
            ):
                best = _better(
                    best,
                    Match(
                        calculate_score(len(query), INSERTION, position),
                        INSERTION,
                        position,
                    ),
                )
                break

            start += 1

    return best


def _better(current: Match | None, candidate: Match) -> Match:
    if current is None or candidate.score > current.score:
        return candidate

    return current
