import sys

from PySide6.QtWidgets import QApplication

from interface.main_window import MainWindow
from interface.mock_search import (
    fake_get_best_k_completions,
)
from interface.styles import APP_STYLE


def main() -> None:
    application = QApplication(sys.argv)
    application.setStyleSheet(APP_STYLE)

    window = MainWindow(
        get_completions=fake_get_best_k_completions
    )
    window.show()

    sys.exit(application.exec())


if __name__ == "__main__":
    main()