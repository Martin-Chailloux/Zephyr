from typing import Self

from PySide6 import QtCore
from PySide6.QtCore import Signal
from PySide6.QtWidgets import QCheckBox, QComboBox, QWidget, QHBoxLayout, QLabel


class ProcessInputBase(QWidget):
    def __init__(self, name: str, label: str):
        super().__init__()
        self.name = name
        self.label = label
        self._init_ui()

    def _init_ui(self):
        layout = QHBoxLayout()
        self.setLayout(layout)

        layout.setAlignment(QtCore.Qt.AlignmentFlag.AlignTop | QtCore.Qt.AlignmentFlag.AlignLeft)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        label_widget = QLabel(self.label)
        label_widget.setFixedWidth(96)
        layout.addWidget(label_widget)

        self.layout = layout
        self.label_widget = label_widget

    def set_enabled(self, is_enabled: bool):
        self.label_widget.setEnabled(is_enabled)

    def to_dict(self) -> dict[str, any]:
        pass

    def import_inputs(self, **kwargs):
        pass


class _CheckBox(QCheckBox):
    enabled_state_changed = Signal(bool)

    def setEnabled(self, is_enabled: bool):
        super().setEnabled(is_enabled)
        self.enabled_state_changed.emit(is_enabled)


class ProcessInputCheckbox(ProcessInputBase):
    def __init__(self, name: str, label: str, is_checked: bool):
        super().__init__(name=name, label=label)
        self._add_checkbox(is_checked=is_checked)

    def _add_checkbox(self, is_checked: bool):
        checkbox = _CheckBox()
        self.layout.addWidget(checkbox)
        checkbox.setChecked(is_checked)
        self.checkbox = checkbox

    def set_enabled(self, is_enabled: bool):
        super().set_enabled(is_enabled)
        self.checkbox.setEnabled(is_enabled)

    def to_dict(self) -> dict[str, any]:
        return {'name': self.name, 'label': self.label, 'value': self.checkbox.isChecked()}

    def import_inputs(self, is_checked: bool):
        self.checkbox.setChecked(is_checked)


class ProcessInputCombobox(ProcessInputBase):
    def __init__(self, name: str, label: str, items: list[str], current_text: str):
        super().__init__(name=name, label=label)
        self._add_combobox(items=items, current_text=current_text)

    def _add_combobox(self, items: list[str], current_text: str):
        combobox = QComboBox()
        self.layout.addWidget(combobox)

        combobox.addItems(items)
        combobox.setCurrentText(current_text)

        self.combobox = combobox

    def set_enabled(self, is_enabled: bool):
        super().set_enabled(is_enabled)
        self.combobox.setEnabled(is_enabled)

    def to_dict(self) -> dict[str, any]:
        items = [self.combobox.itemText(i) for i in range(self.combobox.count())]
        return {'name': self.name, 'label': self.label, 'items': items, 'current_text': self.combobox.currentText()}

    def import_inputs(self, items: list[str], current_text: str):
        self.combobox.clear()
        self.combobox.addItems(items)
        self.combobox.setCurrentText(current_text)
