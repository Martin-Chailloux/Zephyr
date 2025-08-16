from PySide6 import QtCore
from PySide6.QtCore import Signal, Qt
from PySide6.QtWidgets import QVBoxLayout, QPushButton, QHBoxLayout, QDialog, QLineEdit, QLabel, QCheckBox

from Api.breeze_app import BreezeApp
from Api.breeze_converters import BreezeText
from Gui.components.popups.abstract_popup_widget import AbstractPopupWidget
from Utils.pills import GenericPillIcon


# TODO: checkbox to stay on after enter
class LineEditPopup(QDialog):
    create_clicked = Signal(str)

    def __init__(self, title, invalid_entries: list[str] = None, close_on_confirm: bool=False):
        super().__init__()
        self.close_on_confirm = close_on_confirm

        self.setWindowTitle(title)
        self.invalid_names = [] if invalid_entries is None else [BreezeText(t).to_valid_name().lower() for t in invalid_entries]

        self._init_ui()
        self._create_input_buttons()
        self.connect_signals()

        self.on_text_changed()

    @property
    def current_text(self) -> str:
        text = self.line_edit.text()
        return BreezeText(text).to_valid_name()

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
        text = BreezeText(self.current_text).to_valid_name()
        min_length = 1
        max_length = 24
        name_exists = text.lower() in self.invalid_names

        is_valid = False
        color = "orange"
        if len(text) < min_length:
            msg = "Text is empty"
        elif len(text) > max_length:
            msg = "Text is too long"
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


class TextInput:
    def __init__(self, text: str, unavailable_inputs: list[str] = None, min_length: int = 1, max_length: int = 24):
        self.text = text
        self.unavailable_inputs = unavailable_inputs or []
        self.min_length = min_length
        self.max_length = max_length

        self.message = ''

    def set_text(self, text: str):
        self.text = text

    def set_message(self, message: str):
        self.message = message

    @staticmethod
    def _to_output_format(text: str) -> str:
        split_text = text.replace("_", " ").replace("-", " ").split()
        if len(split_text) == 0:
            return text.replace(' ', '')
        else:
            output_text = split_text[0] + "".join(s.title() for s in split_text[1:])
            return output_text

    @property
    def output(self) -> str:
        return self._to_output_format(text=self.text)

    @property
    def is_length_valid(self) -> bool:
        ok = self.min_length < len(self.output) < self.max_length
        if not ok:
            self.set_message(message=f"Invalid length ({len(self.text)}): it should be between {self.min_length} and {self.max_length} chars.")
        return ok

    @property
    def is_available(self) -> bool:
        unavailable = [self._to_output_format(text=s) for s in self.unavailable_inputs]
        ok = self.output not in unavailable
        if not ok:
            self.set_message(message=f"'{self.output}' is not available")
        return ok

    @property
    def is_valid(self) -> bool:
        ok = self.is_length_valid and self.is_available
        if ok:
            self.set_message(message='Text is valid')
        return ok


class TextInputPopup(AbstractPopupWidget):
    accept = Signal()

    def __init__(self, forbidden_inputs: list[str] = None, title: str = "Text Input", placeholder: str = "Input",
                 min_length: int = 1, max_length: int = 24):
        super().__init__(show_borders=True)
        self.setWindowTitle(title)
        self.forbidden_inputs = forbidden_inputs or []
        self.placeholder_text = placeholder

        self.min_length = min_length
        self.max_length = max_length

        self.text_input = TextInput('')

        self._init_ui()
        self._init_state()
        self._connect_signals()

    def _init_ui(self):
        layout = QVBoxLayout()
        self.setLayout(layout)
        layout.setAlignment(QtCore.Qt.AlignmentFlag.AlignTop | QtCore.Qt.AlignmentFlag.AlignLeft)
        layout.setSpacing(0)

        # ------------------------
        # input
        # ------------------------
        sub_layout = QHBoxLayout()
        layout.addLayout(sub_layout)
        sub_layout.setSpacing(7)

        input_pill = GenericPillIcon()
        sub_layout.addWidget(input_pill)

        input_field = QLineEdit()
        sub_layout.addWidget(input_field)
        input_field.setPlaceholderText(self.placeholder_text)

        # ------------------------
        # accept
        # ------------------------
        layout.addSpacing(7)
        accept = QPushButton("Accept")
        layout.addWidget(accept)

        dont_close = QCheckBox("Don't close")
        layout.addWidget(dont_close)

        # ------------------------
        # public vars
        # ------------------------
        self.input_pill = input_pill
        self.input_field = input_field

        self.accept_button = accept
        self.dont_close_checkbox = dont_close

    def _init_state(self):
        self._on_text_changed()

    def _connect_signals(self):
        self.input_field.textChanged.connect(self._on_text_changed)

        self.input_field.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.input_field.customContextMenuRequested.connect(self.reject)

        self.accept_button.clicked.connect(self._on_accept_button_clicked)

    def _on_text_changed(self):
        self.text_input.set_text(text=self.input_field.text())
        if self.text_input.is_valid:
            self.input_pill.set_true()
        else:
            self.input_pill.set_false()
        self.input_pill.setToolTip(self.text_input.message)

        self.accept_button.setEnabled(self.text_input.is_valid)
        if not self.text_input.is_valid:
            self.accept_button.setText(f"Needs a valid input")
        else:
            self.accept_button.setText(f"{self.text_input.output}")

    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key.Key_Return:
            if self.accept_button.isEnabled():
                self.accept_button.clicked.emit()

        elif event.key() == QtCore.Qt.Key.Key_Escape:
            self.accept_button.clicked.emit()

        else:
            super().keyPressEvent(event)

    def _on_accept_button_clicked(self):
        self.accept.emit()
        self.input_field.clear()
        if not self.dont_close_checkbox.isChecked():
            self.close()