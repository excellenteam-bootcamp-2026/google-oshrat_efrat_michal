from dataclasses import dataclass

@dataclass(slots=True)
class Sentence:
    id: int
    text: str
    normalized_text: str
    tokens: list[str]
    file_path: str
    line_number: int