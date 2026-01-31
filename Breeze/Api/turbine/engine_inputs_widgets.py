from dataclasses import dataclass

from PySide6 import QtCore
from PySide6.QtWidgets import QCheckBox, QComboBox, QWidget, QHBoxLayout, QLabel

from Api.turbine.utils import JobContext


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

    def to_dict(self) -> dict[str, any]:
        pass

    def from_dict(self, **kwargs):
        # TODO when implementing process relaunch from turbine gui (in sub-classes)
        pass


class Checkbox(TurbineWidgetBase):
    def __init__(self, name: str, label: str, is_checked: bool):
        super().__init__(name=name, label=label)
        checkbox = QCheckBox()
        self.layout.addWidget(checkbox)
        checkbox.setChecked(is_checked)
        self.checkbox = checkbox

    def set_enabled(self, is_enabled: bool):
        super().set_enabled(is_enabled)
        self.checkbox.setEnabled(is_enabled)

    def to_dict(self) -> dict[str, any]:
        return {'label': self.label, 'value': self.checkbox.isChecked()}

    def from_dict(self, is_checked: bool):
        self.checkbox.setChecked(is_checked)


class Combobox(TurbineWidgetBase):
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

    def to_dict(self) -> dict[str, any]:
        items = [self.combobox.itemText(i) for i in range(self.combobox.count())]
        return {'label': self.label, 'items': items, 'current_text': self.combobox.currentText()}

    def from_dict(self, items: list[str], current_text: str):
        self.combobox.clear()
        self.combobox.addItems(items)
        self.combobox.setCurrentText(current_text)


class DontOverwriteCheckbox(Checkbox):
    def __init__(self):
        super().__init__(name='dont_overwrite', label='Dont overwrite', is_checked=True)

class LastVersionCheckbox(Checkbox):
    def __init__(self):
        super().__init__(name='last_version', label='Last version', is_checked=True)


class VersionNumberCombobox(Combobox):
    def __init__(self, context: JobContext):
        numbers: list[str] = [f"{i:03d}" for i in context.component.get_version_numbers()]
        if context.version is None:
            selected_number: str = ''
        else:
            selected_number: str = f"{context.version.number:03d}"
        super().__init__(name='version_num', label='Version num', items=numbers, current_text=selected_number)


@dataclass
class Generics:
    Checkbox = Checkbox
    Combobox = Combobox

@dataclass
class Specifics:
    DontOverwrite = DontOverwriteCheckbox
    LastVersion = LastVersionCheckbox
    VersionNumber = VersionNumberCombobox
