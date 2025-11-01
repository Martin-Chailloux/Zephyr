from dataclasses import dataclass

from PySide6 import QtCore
from PySide6.QtWidgets import QCheckBox, QComboBox, QWidget, QHBoxLayout, QLabel


class TurbineWidgetBase(QWidget):
    """ A base layout with a label, to be extended with a control widget """
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

    def export_infos(self) -> dict[str, any]:
        pass

    def import_inputs(self, **kwargs):
        pass


class TurbineWidgetCheckbox(TurbineWidgetBase):
    def __init__(self, name: str, label: str, is_checked: bool):
        super().__init__(name=name, label=label)
        checkbox = QCheckBox()
        self.layout.addWidget(checkbox)
        checkbox.setChecked(is_checked)
        self.checkbox = checkbox

    def set_enabled(self, is_enabled: bool):
        super().set_enabled(is_enabled)
        self.checkbox.setEnabled(is_enabled)

    def export_infos(self) -> dict[str, any]:
        return {'label': self.label, 'value': self.checkbox.isChecked()}

    def import_inputs(self, is_checked: bool):
        self.checkbox.setChecked(is_checked)


class TurbineWidgetCombobox(TurbineWidgetBase):
    def __init__(self, name: str, label: str, items: list[str], current_text: str):
        super().__init__(name=name, label=label)
        combobox = QComboBox()
        self.layout.addWidget(combobox)

        combobox.addItems(items)
        combobox.setCurrentText(current_text)

        self.combobox = combobox

    def set_enabled(self, is_enabled: bool):
        super().set_enabled(is_enabled)
        self.combobox.setEnabled(is_enabled)

    def export_infos(self) -> dict[str, any]:
        items = [self.combobox.itemText(i) for i in range(self.combobox.count())]
        return {'label': self.label, 'items': items, 'current_text': self.combobox.currentText()}

    def import_inputs(self, items: list[str], current_text: str):
        self.combobox.clear()
        self.combobox.addItems(items)
        self.combobox.setCurrentText(current_text)


@dataclass
class TurbineWidgets:
    Checkbox = TurbineWidgetCheckbox
    Combobox = TurbineWidgetCombobox
