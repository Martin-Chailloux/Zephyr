from PySide6 import QtCore
from PySide6.QtCore import Signal
from PySide6.QtWidgets import QVBoxLayout, QPushButton, QHBoxLayout, QDialog, QLineEdit, QLabel

from MangoEngine import mongo_dialog


class LineEditPopup(QDialog):
    create_clicked = Signal(str)

    def __init__(self, title, invalid_entries: list[str] = None):
        super().__init__()
        self.setWindowTitle(title)
        self.invalid_names = [] if invalid_entries is None else [mongo_dialog.text_to_input(t).lower() for t in invalid_entries]

        self._init_ui()
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

        h_layout = QHBoxLayout()
        layout.addLayout(h_layout)

        cancel_button = QPushButton("Cancel")
        h_layout.addWidget(cancel_button)

        create_button = QPushButton("Create")
        h_layout.addWidget(create_button)
        create_button.clicked.connect(self.on_create_clicked)

        for button in [cancel_button, create_button]:
            button.clicked.connect(self.close)

        self.warning_label = warning_label
        self.line_edit = line_edit
        self.create_button = create_button
        self.cancel_button = cancel_button

    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key.Key_Return:
            if self.create_button.isEnabled():
                self.create_button.clicked.emit()
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
        self.create_button.setEnabled(is_valid)

    def on_create_clicked(self):
        self.create_clicked.emit(self.current_text)

