from dataclasses import dataclass

from models.sentence import Sentence

@dataclass
class SearchResult:
    sentence: Sentence
    score: float
    match_type: str = "exact"
    error_position: int | None = None
