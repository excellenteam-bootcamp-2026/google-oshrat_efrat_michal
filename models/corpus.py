from dataclasses import dataclass

from models.sentence import Sentence
from models.occurrence import Occurrence

@dataclass
class Corpus:
    sentences: dict[int, Sentence]
    word_index: dict[str, list[Occurrence]]