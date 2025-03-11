from PySide6.QtCore import Signal
from PySide6.QtWidgets import QWidget, QHBoxLayout, QLineEdit


class SearchbarWidget(QWidget):
    text_changed = Signal(str)

    def __init__(self):
        super().__init__()
        self._init_ui()

    def _init_ui(self):
        layout = QHBoxLayout()
        self.setLayout(layout)

        line_edit = QLineEdit()
        layout.addWidget(line_edit)

        self._searchbar = line_edit

    def _connect_signals(self):
        self._searchbar.textChanged.connect(self.text_changed.emit)