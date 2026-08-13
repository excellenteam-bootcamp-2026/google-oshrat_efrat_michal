from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QLabel,
    QSizePolicy,
    QVBoxLayout,
)

# בעת החיבור הסופי יש לייבא את AutoCompleteData
# מהקובץ המשותף של הצוות.
from interface.mock_search import AutoCompleteData


class ResultCard(QFrame):
    def __init__(
        self,
        index: int,
        result: AutoCompleteData,
        parent=None
    ) -> None:
        super().__init__(parent)

        self.setObjectName("resultCard")
        self.setSizePolicy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Fixed
        )

        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(18, 14, 18, 12)
        main_layout.setSpacing(12)

        number_label = QLabel(str(index))
        number_label.setObjectName("resultNumber")
        number_label.setFixedSize(30, 30)
        main_layout.addWidget(
            number_label,
            alignment=Qt.AlignmentFlag.AlignTop
        )

        information_layout = QVBoxLayout()
        information_layout.setSpacing(4)

        sentence_label = QLabel(result.completed_sentence)
        sentence_label.setObjectName("sentence")
        sentence_label.setWordWrap(True)
        sentence_label.setTextInteractionFlags(
            Qt.TextInteractionFlag.TextSelectableByMouse
        )
        information_layout.addWidget(sentence_label)

        source_label = QLabel(
            f"{result.source_text} · offset {result.offset}"
        )
        source_label.setObjectName("sourceText")
        source_label.setWordWrap(True)
        source_label.setTextInteractionFlags(
            Qt.TextInteractionFlag.TextSelectableByMouse
        )
        information_layout.addWidget(source_label)

        main_layout.addLayout(information_layout, stretch=1)

        score_label = QLabel(str(result.score))
        score_label.setObjectName("score")
        score_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        main_layout.addWidget(
            score_label,
            alignment=Qt.AlignmentFlag.AlignTop
        )