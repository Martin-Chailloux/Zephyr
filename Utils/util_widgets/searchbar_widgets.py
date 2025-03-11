from PySide6 import QtCore
from PySide6.QtCore import Signal
from PySide6.QtWidgets import QWidget, QHBoxLayout, QLineEdit, QPushButton


class SearchbarWidget(QWidget):
    text_changed = Signal(str)

    def __init__(self):
        super().__init__()
        self._init_ui()
        self._connect_signals()
        self._set_initial_state()

    def _init_ui(self):
        layout = QHBoxLayout()
        self.setLayout(layout)
        layout.setAlignment(QtCore.Qt.AlignmentFlag.AlignLeft)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        line_edit = QLineEdit()
        layout.addWidget(line_edit)
        line_edit.setPlaceholderText("Search")

        self._line_edit = line_edit

    def _connect_signals(self):
        self._line_edit.textChanged.connect(self.text_changed.emit)

    def _on_text_changed(self, text: str):
        self.text_changed.emit(text)

    def _set_initial_state(self):
        self._line_edit.setMaximumWidth(172)
