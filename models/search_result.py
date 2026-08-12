from dataclasses import dataclass

from models.sentence import Sentence

@dataclass
class SearchResult:
    sentence: Sentence
    score: float