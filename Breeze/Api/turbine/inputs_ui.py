from dataclasses import dataclass

from PySide6 import QtCore
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel

from Api.document_models.project_documents import JobContext
from Api.turbine.inputs_widgets import ProcessInputCheckbox, ProcessInputCombobox


@dataclass
class ProcessInputs:
    last_version: bool = False
    version_number: int = None


class ProcessInputsUi(QWidget):
    def __init__(self, label: str, context: JobContext = None):
        super().__init__()
        self.label = label
        self.Context = context
        self.input_widgets = []

        layout = QVBoxLayout()
        self.setLayout(layout)

        layout.setAlignment(QtCore.Qt.AlignmentFlag.AlignTop | QtCore.Qt.AlignmentFlag.AlignLeft)
        layout.setContentsMargins(0, 0, 0, 0)

        title = QLabel(self.label)
        layout.addWidget(title)

        sub_layout = QVBoxLayout()
        layout.addLayout(sub_layout)
        sub_layout.setContentsMargins(7, 7, 7, 7)
        sub_layout.setSpacing(3)

        self.layout = sub_layout

    def add_checkbox(self, name: str, label: str, is_checked: bool=False) -> ProcessInputCheckbox:
        checkbox = ProcessInputCheckbox(name=name, label=label, is_checked=is_checked)
        self.input_widgets.append(checkbox)
        self.layout.addWidget(checkbox)
        return checkbox

    def add_combobox(self, name: str, label: str, items: list[str], current_text: str='') -> ProcessInputCombobox:
        combobox = ProcessInputCombobox(name=name, label=label, items=items, current_text=current_text)
        self.input_widgets.append(combobox)
        self.layout.addWidget(combobox)
        return combobox

    def to_dict(self) -> list[dict[str, any]]:
        widget_infos = []
        for widget in self.input_widgets:
            widget_infos.append(widget.to_database())
        return widget_infos

    @property
    def inputs(self) -> ProcessInputs:
        return ProcessInputs()

    @classmethod
    def from_dict(cls, widgets: list[dict[str, any]]):
        process_inputs = cls()

        for infos in widgets:
            widget_type = infos['widget']
            if widget_type is None:
                return

            name=infos['name']
            label=infos['label']

            if widget_type == 'checkbox':
                process_inputs.add_checkbox(name=name, label=label, is_checked=infos.get('is_checked', False))
            elif widget_type == 'combobox':
                process_inputs.add_combobox(name=name, label=label, items=infos.get('items', []), current_text=infos.get('current_text', ''))
