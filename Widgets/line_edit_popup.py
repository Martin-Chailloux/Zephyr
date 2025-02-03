from PySide6 import QtCore
from PySide6.QtCore import Signal
from PySide6.QtWidgets import QVBoxLayout, QPushButton, QHBoxLayout, QDialog, QLineEdit, QLabel

from MangoEngine import mongo_dialog

class LineEditPopup(QDialog):
    create_clicked = Signal(str)

    def __init__(self, title, invalid_entries: list[str] = None, close_on_confirm: bool=False):
        super().__init__()
        self.close_on_confirm = close_on_confirm

        self.setWindowTitle(title)
        self.invalid_names = [] if invalid_entries is None else [mongo_dialog.text_to_input(t).lower() for t in invalid_entries]

        self._init_ui()
        self._create_input_buttons()
        self.connect_signals()

        self.on_text_changed()

    @property
    def current_text(self) -> str:
        text = self.line_edit.text()
        return mongo_dialog.text_to_input(text)

    def _init_ui(self):
        layout = QVBoxLayout()
        self.setLayout(layout)
        layout.setAlignment(QtCore.Qt.AlignmentFlag.AlignTop | QtCore.Qt.AlignmentFlag.AlignLeft)

        warning_label = QLabel()
        layout.addWidget(warning_label)

        line_edit = QLineEdit()
        layout.addWidget(line_edit)
        line_edit.textChanged.connect(self.on_text_changed)

        self.layout = layout
        self.warning_label = warning_label
        self.line_edit = line_edit

    def _create_input_buttons(self):
        h_layout = QHBoxLayout()
        self.layout.addLayout(h_layout)

        cancel_button = QPushButton("Cancel")
        h_layout.addWidget(cancel_button)

        confirm_button = QPushButton("Create")
        h_layout.addWidget(confirm_button)

        self.confirm_button = confirm_button
        self.cancel_button = cancel_button

    def connect_signals(self):
        if self.close_on_confirm:
            self.confirm_button.clicked.connect(self.close)
        self.cancel_button.clicked.connect(self.close)
        self.confirm_button.clicked.connect(self.on_create_clicked)

    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key.Key_Return:
            if self.confirm_button.isEnabled():
                self.confirm_button.clicked.emit()
        elif event.key() == QtCore.Qt.Key.Key_Escape:
            self.cancel_button.clicked.emit()
        else:
            super().keyPressEvent(event)

    def on_text_changed(self):
        text = mongo_dialog.text_to_input(self.current_text)
        min_length = 1
        max_length = 12
        name_exists = text.lower() in self.invalid_names

        is_valid = False
        color = "orange"
        if len(text) < min_length:
            msg = "Not enough characters"
        elif len(text) > max_length:
            msg = "Too many characters"
        elif name_exists:
            msg = "Name already exist"

        else:
            is_valid = True
            msg = "Valid name"
            color = "lightgreen"

        self.warning_label.setText(msg)
        self.warning_label.setStyleSheet(f"color: {color}")
        self.confirm_button.setEnabled(is_valid)

    def on_create_clicked(self):
        self.create_clicked.emit(self.current_text)
        self.line_edit.clear()
