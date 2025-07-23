from typing import Self

from PySide6.QtCore import Signal
from PySide6.QtWidgets import QCheckBox, QComboBox


class InputCheckBox(QCheckBox):
    enabled_state_changed = Signal(bool)

    def __init__(self, name: str, label: str, value: bool = False):
        super().__init__()
        self.name = name
        self.label = label
        self.setChecked(value)

    def setEnabled(self, is_enabled: bool):
        super().setEnabled(is_enabled)
        self.enabled_state_changed.emit(is_enabled)

    def to_dict(self) -> dict[str, any]:
        return {'name': self.name, 'label': self.label, 'value': self.isChecked()}

    @classmethod
    def from_dict(cls, infos: dict[str, any]) -> Self:
        checkbox = cls(name=infos['name'], label=infos['label'], value=infos.get('value', False))
        return checkbox


class InputComboBox(QComboBox):
    enabled_state_changed = Signal(bool)

    def __init__(self, name: str, label: str, items: list[str], value: str = ''):
        super().__init__()
        self.name = name
        self.label = label
        self.addItems(items)
        self.setCurrentText(value)

    def setEnabled(self, is_enabled: bool):
        super().setEnabled(is_enabled)
        self.enabled_state_changed.emit(is_enabled)

    def to_dict(self) -> dict[str, any]:
        items = [self.itemText(i) for i in range(self.count())]
        return {'name': self.name, 'label': self.label, 'items': items, 'value': self.currentText()}

    @classmethod
    def from_dict(cls, infos: dict[str, any]) -> Self:
        combobox = cls(name=infos['name'], label=infos['label'], items=infos['items'], value=infos.get('value', ''))
        return combobox
