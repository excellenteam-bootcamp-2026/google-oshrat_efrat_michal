from dataclasses import dataclass

@dataclass(slots=True)
class Occurrence:
    sentence_id: int
    position: int