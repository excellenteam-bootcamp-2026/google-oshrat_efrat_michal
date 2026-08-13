from collections.abc import Callable

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QScrollArea,
    QSizePolicy,
    QVBoxLayout,
    QWidget,
)

from interface.autocomplete_data import AutoCompleteData
from interface.result_card import ResultCard


class MainWindow(QMainWindow):
    def __init__(
        self,
        get_completions: Callable[
            [str],
            list[AutoCompleteData]
        ]
    ) -> None:
        super().__init__()

        self.get_completions = get_completions
        self.current_sentence = ""

        self.configure_window()
        self.create_interface()

    def configure_window(self) -> None:
        self.setWindowTitle("Sentence AutoComplete")
        self.resize(900, 650)
        self.setMinimumSize(720, 520)

    def create_interface(self) -> None:
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        page_layout = QVBoxLayout(central_widget)
        page_layout.setContentsMargins(0, 0, 0, 0)
        page_layout.setSpacing(0)

        page_layout.addWidget(self.create_header())
        page_layout.addWidget(
            self.create_main_content(),
            stretch=1
        )

    def create_header(self) -> QFrame:
        header = QFrame()
        header.setObjectName("header")
        header.setFixedHeight(104)

        layout = QVBoxLayout(header)
        layout.setContentsMargins(32, 16, 32, 8)
        layout.setSpacing(4)
        layout.setAlignment(Qt.AlignmentFlag.AlignLeft)

        title_row = QHBoxLayout()
        title_row.setContentsMargins(0, 0, 0, 0)
        title_row.setSpacing(8)

        logo = QLabel("S")
        logo.setObjectName("brandLogo")
        logo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        logo.setFixedSize(22, 22)

        title = QLabel("Sentence AutoComplete")
        title.setObjectName("title")
        title.setAlignment(Qt.AlignmentFlag.AlignVCenter)

        title_row.addWidget(logo)
        title_row.addWidget(title)
        title_row.addStretch(1)

        subtitle = QLabel(
            "Find the best completion for your sentence"
        )
        subtitle.setObjectName("subtitle")
        subtitle.setAlignment(Qt.AlignmentFlag.AlignLeft)

        layout.addLayout(title_row)
        layout.addWidget(subtitle)
        layout.addStretch(1)

        return header

    def create_main_content(self) -> QWidget:
        container = QWidget()

        layout = QVBoxLayout(container)
        layout.setContentsMargins(32, 20, 32, 24)
        layout.setSpacing(10)

        layout.addWidget(
            self.create_search_card(),
            alignment=Qt.AlignmentFlag.AlignHCenter
        )
        layout.addWidget(self.create_results_header())
        layout.addWidget(
            self.create_results_area(),
            stretch=1
        )

        return container

    def create_search_card(self) -> QFrame:
        card = QFrame()
        card.setObjectName("searchCard")
        card.setMaximumWidth(1060)
        card.setMinimumWidth(620)
        card.setSizePolicy(
            QSizePolicy.Policy.Preferred,
            QSizePolicy.Policy.Fixed
        )

        layout = QVBoxLayout(card)
        layout.setContentsMargins(0, 8, 0, 8)
        layout.setSpacing(8)

        search_shell = QFrame()
        search_shell.setObjectName("searchShell")

        input_row = QHBoxLayout(search_shell)
        input_row.setContentsMargins(14, 0, 0, 0)
        input_row.setSpacing(0)

        search_icon = QLabel("⌕")
        search_icon.setObjectName("searchIcon")
        input_row.addWidget(search_icon)

        self.search_input = QLineEdit()
        self.search_input.setObjectName("searchInput")
        self.search_input.setPlaceholderText(
            "Type the beginning of a sentence..."
        )
        self.search_input.returnPressed.connect(self.search)
        input_row.addWidget(self.search_input, stretch=1)

        search_button = QPushButton("Search")
        search_button.setObjectName("searchButton")
        search_button.setToolTip("Search")
        search_button.setFocusPolicy(
            Qt.FocusPolicy.NoFocus
        )
        search_button.clicked.connect(self.search)
        input_row.addWidget(search_button)

        layout.addWidget(search_shell)

        self.current_sentence_label = QLabel("")
        self.current_sentence_label.setObjectName("secondaryText")
        self.current_sentence_label.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )
        self.current_sentence_label.hide()
        layout.addWidget(self.current_sentence_label)

        self.reset_button = QPushButton("New sentence")
        self.reset_button.setObjectName("resetButton")
        self.reset_button.clicked.connect(self.reset_sentence)
        layout.addWidget(
            self.reset_button,
            alignment=Qt.AlignmentFlag.AlignHCenter
        )

        return card

    def create_results_header(self) -> QWidget:
        self.results_header = QWidget()

        layout = QHBoxLayout(self.results_header)
        layout.setContentsMargins(5, 0, 5, 4)

        title = QLabel("Best completions")
        title.setObjectName("sectionTitle")
        layout.addWidget(title)

        layout.addStretch()

        self.results_count_label = QLabel("")
        self.results_count_label.setObjectName("resultsCount")
        layout.addWidget(self.results_count_label)

        self.results_header.hide()

        return self.results_header

    def create_results_area(self) -> QScrollArea:
        scroll_area = QScrollArea()
        self.results_area = scroll_area
        self.results_area.hide()

        scroll_area.setWidgetResizable(True)
        scroll_area.setFrameShape(
            QFrame.Shape.NoFrame
        )

        self.results_widget = QFrame()
        self.results_widget.setObjectName("resultsBox")

        self.results_layout = QVBoxLayout(
            self.results_widget
        )
        self.results_layout.setContentsMargins(0, 0, 0, 0)
        self.results_layout.setSpacing(0)
        self.results_layout.setAlignment(
            Qt.AlignmentFlag.AlignTop
        )

        scroll_area.setWidget(self.results_widget)

        return scroll_area

    def search(self) -> None:
        user_input = self.search_input.text()

        if user_input.strip() == "#":
            self.reset_sentence()
            return

        if not user_input.strip():
            QMessageBox.warning(
                self,
                "Missing text",
                "Please enter some text before searching."
            )
            return

        # אם כבר קיים משפט, מוסיפים רווח לפני ההמשך.
        if self.current_sentence:
            self.current_sentence += " " + user_input.strip()
        else:
            self.current_sentence = user_input.strip()

        self.search_input.clear()

        self.current_sentence_label.setText(
            f"Current sentence: {self.current_sentence}"
        )
        self.current_sentence_label.show()

        try:
            results = self.get_completions(
                self.current_sentence
            )
            self.display_results(results)

        except Exception as error:
            QMessageBox.critical(
                self,
                "Search error",
                f"An error occurred:\n{error}"
            )

    def display_results(
        self,
        results: list[AutoCompleteData]
    ) -> None:
        displayed_results = results[:5]

        if not displayed_results:
            self.results_header.hide()
            self.results_area.hide()

            QMessageBox.information(
                self,
                "No results",
                "No completions were found."
            )
            return

        self.clear_results()

        self.results_count_label.setText(
            f"{len(displayed_results)} results"
        )

        for index, result in enumerate(
            displayed_results,
            start=1
        ):
            card = ResultCard(index, result)
            self.results_layout.addWidget(card)

            if index < len(displayed_results):
                divider = QFrame()
                divider.setObjectName("resultDivider")
                divider.setFrameShape(
                    QFrame.Shape.HLine
                )
                self.results_layout.addWidget(divider)

        self.results_header.show()
        self.results_area.show()

    def reset_sentence(self) -> None:
        self.current_sentence = ""
        self.search_input.clear()

        self.current_sentence_label.clear()
        self.current_sentence_label.hide()

        self.results_count_label.clear()
        self.results_header.hide()
        self.results_area.hide()

        self.clear_results()

        self.search_input.setFocus()

    def clear_results(self) -> None:
        while self.results_layout.count():
            item = self.results_layout.takeAt(0)

            widget = item.widget()

            if widget is not None:
                widget.deleteLater()

    def show_message(self, message: str) -> None:
        self.clear_results()

        label = QLabel(message)
        label.setObjectName("secondaryText")
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        label.setWordWrap(True)
        label.setSizePolicy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Fixed
        )

        self.results_layout.addWidget(label)