from PySide6 import QtCore
from PySide6.QtCore import Signal, Qt
from PySide6.QtWidgets import QVBoxLayout, QPushButton, QHBoxLayout, QLineEdit, QCheckBox

from Gui.components.popups.abstract_popup_widget import AbstractPopupWidget
from Utils.pills import GenericPillIcon


class _TextInput:
    def __init__(self, text: str, forbidden_inputs: list[str] = None, min_length: int = 1, max_length: int = 24):
        self.text = text
        self.forbidden_inputs = forbidden_inputs or []
        self.forbidden_inputs = [self._to_output_format(text=s) for s in self.forbidden_inputs]
        self.forbidden_inputs = [s.lower() for s in self.forbidden_inputs]
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
    def is_too_short(self) -> bool:
        ok = len(self.output) < self.min_length
        if not ok:
            self.set_message(message=f"Length ({len(self.text)}) is too short : it should be higher than {self.min_length} chars.")
        return ok

    @property
    def is_too_long(self) -> bool:
        ok = len(self.output) > self.max_length
        if not ok:
            self.set_message(message=f"Length ({len(self.text)}) is too long : it should be lower than {self.min_length} chars.")
        return ok

    @property
    def is_available(self) -> bool:
        ok = self.output.lower() not in self.forbidden_inputs
        if not ok:
            self.set_message(message=f"'{self.output}' is not available.")
        return ok

    @property
    def is_valid(self) -> bool:
        ok = not self.is_too_short and not self.is_too_long and self.is_available
        if ok:
            self.set_message(message='Text is valid')
        return ok


class TextInputPopup(AbstractPopupWidget):
    input_accepted = Signal(str)

    def __init__(self, forbidden_inputs: list[str] = None, title: str = "Text Input", placeholder: str = "Input",
                 min_length: int = 1, max_length: int = 24,
                 dont_close: bool = False):
        super().__init__(show_borders=True)
        self.setWindowTitle(title)
        self.forbidden_inputs = forbidden_inputs or []
        self.placeholder_text = placeholder
        self.init_dont_close = dont_close

        self.min_length = min_length
        self.max_length = max_length

        self.text_input = _TextInput('', forbidden_inputs=self.forbidden_inputs)

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
        self.dont_close_checkbox.setChecked(self.init_dont_close)

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
        if self.text_input.is_too_short:
            self.accept_button.setText(f"Too short")
        elif self.text_input.is_too_long:
            self.accept_button.setText(f"Too long")
        elif not self.text_input.is_available:
            self.accept_button.setText(f"Not available")
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
        self.input_accepted.emit(self.text_input.output)
        self.input_field.clear()

        if not self.dont_close_checkbox.isChecked():
            self.close()
