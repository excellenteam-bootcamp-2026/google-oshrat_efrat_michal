from dataclasses import dataclass


@dataclass
class AutoCompleteData:
    completed_sentence: str
    source_text: str
    offset: int
    score: int


def fake_get_best_k_completions(
    prefix: str
) -> list[AutoCompleteData]:
    """
    פונקציית דמה זמנית.

    בהמשך נחליף אותה בפונקציית החיפוש האמיתית
    של אדם ב׳.
    """
    return [
        AutoCompleteData(
            completed_sentence=f"{prefix} is a search engine",
            source_text="data/google.txt",
            offset=10,
            score=95
        ),
        AutoCompleteData(
            completed_sentence=f"{prefix} provides many services",
            source_text="data/services.txt",
            offset=25,
            score=85
        ),
        AutoCompleteData(
            completed_sentence=f"{prefix} was founded in 1998",
            source_text="data/history.txt",
            offset=41,
            score=75
        ),
        AutoCompleteData(
            completed_sentence=(
                f"{prefix} can help users find information"
            ),
            source_text="data/information.txt",
            offset=56,
            score=68
        ),
        AutoCompleteData(
            completed_sentence=f"{prefix} is used around the world",
            source_text="data/world.txt",
            offset=72,
            score=60
        )
    ]