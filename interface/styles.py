APP_STYLE = """
QMainWindow {
    background-color: #EEF4FF;
}

QWidget {
    color: #172033;
    font-family: "Segoe UI";
    font-size: 14px;
}

/* Header */

QFrame#header {
    background-color: transparent;
}

QLabel#brandLogo {
    color: #1D4ED8;
    background-color: qlineargradient(
        x1:0, y1:0, x2:0, y2:1,
        stop:0 #F7FBFF,
        stop:1 #E6F0FF
    );
    border: 1px solid #D4E2F5;
    border-radius: 11px;
    font-size: 12px;
    font-weight: 700;
}

QLabel#title {
    color: #172033;
    font-size: 15px;
    font-weight: 600;
}

QLabel#subtitle {
    color: #7A8494;
    font-size: 12px;
}

/* Search area */

QFrame#searchCard {
    background-color: transparent;
    border: none;
}

QFrame#searchShell {
    background-color: qlineargradient(
        x1:0, y1:0, x2:0, y2:1,
        stop:0 #FFFFFF,
        stop:0.48 #F9FCFF,
        stop:1 #EDF5FF
    );
    border: 1px solid #D5E3F5;
    border-radius: 20px;
}

QFrame#searchShell:focus-within {
    border-color: #60A5FA;
}

QLabel#searchIcon {
    color: #7A8494;
    font-size: 20px;
    padding-left: 6px;
    padding-right: 12px;
}

QLineEdit#searchInput {
    min-height: 34px;
    padding: 14px 2px 14px 0;
    color: #172033;
    background-color: transparent;
    border: none;
    font-size: 16px;
    selection-background-color: #3B82F6;
}

QLineEdit#searchInput::placeholder {
    color: #7A8494;
}

QLineEdit#searchInput:focus {
    background-color: transparent;
}

QPushButton#searchButton {
    min-width: 120px;
    min-height: 64px;
    max-width: 120px;
    max-height: 64px;
    color: #FFFFFF;
    background-color: qlineargradient(
        x1:0, y1:0, x2:0, y2:1,
        stop:0 #60A5FA,
        stop:0.52 #3B82F6,
        stop:1 #2563EB
    );
    border: none;
    border-left: 1px solid #C9DBF2;
    border-top-right-radius: 20px;
    border-bottom-right-radius: 20px;
    font-size: 15px;
    font-weight: 600;
}

QPushButton#searchButton:hover {
    background-color: qlineargradient(
        x1:0, y1:0, x2:0, y2:1,
        stop:0 #7DB7FF,
        stop:0.5 #4C8EF7,
        stop:1 #2D6BED
    );
}

QPushButton#searchButton:pressed {
    background-color: qlineargradient(
        x1:0, y1:0, x2:0, y2:1,
        stop:0 #2D6BED,
        stop:1 #1D4ED8
    );
}

QPushButton#resetButton {
    padding: 4px 8px;
    color: #7A8494;
    background-color: transparent;
    border: none;
    font-size: 13px;
    font-weight: 600;
}

QPushButton#resetButton:hover {
    color: #2563EB;
}

QFrame#resultsBox {
    background-color: qlineargradient(
        x1:0, y1:0, x2:0, y2:1,
        stop:0 #FFFFFF,
        stop:1 #F8FBFF
    );
    border: 1px solid #DBE6F5;
    border-radius: 14px;
}

QLabel#sectionTitle {
    color: #172033;
    font-size: 16px;
    font-weight: 700;
}

QLabel#resultsCount {
    color: #1D4ED8;
    background-color: qlineargradient(
        x1:0, y1:0, x2:0, y2:1,
        stop:0 #F3F9FF,
        stop:1 #E3F0FF
    );
    border-radius: 10px;
    padding: 4px 10px;
    font-size: 12px;
    font-weight: 600;
}

QLabel#secondaryText {
    color: #7A8494;
}

QFrame#resultCard {
    background-color: transparent;
    border: none;
}

QLabel#resultNumber {
    color: #2563EB;
    background-color: qlineargradient(
        x1:0, y1:0, x2:0, y2:1,
        stop:0 #F4FAFF,
        stop:1 #E6F1FF
    );
    border-radius: 12px;
    font-size: 12px;
    font-weight: 700;
}

QLabel#sentence {
    color: #172033;
    font-size: 15px;
    font-weight: 600;
}

QLabel#sourceText {
    color: #7A8494;
    font-size: 12px;
}

QLabel#score {
    color: #15803D;
    background-color: qlineargradient(
        x1:0, y1:0, x2:0, y2:1,
        stop:0 #F3FFF8,
        stop:1 #DCFCE7
    );
    border-radius: 10px;
    padding: 6px 10px;
    font-weight: 700;
}

QFrame#resultDivider {
    border: none;
    border-top: 1px solid #E2E8F0;
    margin-left: 16px;
    margin-right: 16px;
}

QScrollArea {
    background-color: transparent;
    border: none;
}

QScrollArea > QWidget > QWidget {
    background-color: transparent;
}

QScrollBar:vertical {
    width: 7px;
    background: transparent;
}

QScrollBar::handle:vertical {
    min-height: 30px;
    background-color: qlineargradient(
        x1:0, y1:0, x2:0, y2:1,
        stop:0 #D6E5F7,
        stop:1 #BDD2EB
    );
    border-radius: 3px;
}

QScrollBar::add-line:vertical,
QScrollBar::sub-line:vertical {
    height: 0;
}
"""