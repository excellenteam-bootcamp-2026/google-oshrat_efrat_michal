import sys
from pathlib import Path

from PySide6.QtWidgets import QApplication

from archive_reader.reader import build_corpus
from interface.main_window import MainWindow
from interface.autocomplete_data import AutoCompleteData
from interface.styles import APP_STYLE
from search_logic.autocomplete_service import (
    AutocompleteService,
)


ARCHIVE_PATH = (
    Path(__file__).resolve().parents[1]
    / "data"
    / "Archive.zip"
)


def _build_real_completion_handler():
    corpus = build_corpus(str(ARCHIVE_PATH))
    service = AutocompleteService(corpus)

    def get_best_k_completions(
        sentence_prefix: str,
    ) -> list[AutoCompleteData]:
        results = service.search(sentence_prefix, limit=5)

        return [
            AutoCompleteData(
                completed_sentence=result.sentence.text,
                source_text=result.sentence.file_path,
                offset=result.sentence.line_number,
                score=int(round(result.score)),
            )
            for result in results
        ]

    return get_best_k_completions


def main() -> None:
    application = QApplication(sys.argv)
    application.setStyleSheet(APP_STYLE)

    get_completions = _build_real_completion_handler()

    window = MainWindow(
        get_completions=get_completions
    )
    window.show()

    sys.exit(application.exec())


if __name__ == "__main__":
    main()