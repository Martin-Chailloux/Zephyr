from PySide6 import QtCore
from PySide6.QtWidgets import QWidget, QHBoxLayout, QLabel, QVBoxLayout

from Api.project_documents import JobContext
from Api.turbine.inputs_widgets import InputCheckBox, InputComboBox


class ProcessInputsUi(QWidget):
    def __init__(self, context: JobContext = None):
        super().__init__()
        self.Context = context
        self.input_widgets = []

        layout = QVBoxLayout()
        self.setLayout(layout)

        layout.setAlignment(QtCore.Qt.AlignmentFlag.AlignTop | QtCore.Qt.AlignmentFlag.AlignLeft)
        layout.setSpacing(0)

        self.layout = layout

    def _add_widget(self, label: str, widget: QWidget) -> QWidget:
        h_layout = QHBoxLayout()
        self.layout.addLayout(h_layout)

        label = QLabel(label)
        label.setFixedWidth(96)
        h_layout.addWidget(label)

        h_layout.addWidget(widget)
        # TODO: currently 'enabled_state_changed' needs to be defined in every subwidget, there must be a better way
        #  the goal is to match the label enabled state with its associated widget
        widget.enabled_state_changed.connect(label.setEnabled)

        return widget

    def add_checkbox(self, name: str, label: str, value: bool=False) -> InputCheckBox:
        checkbox = InputCheckBox(name=name, label=label, value=value)
        self.input_widgets.append(checkbox)
        self._add_widget(label=label, widget=checkbox)
        return checkbox

    def add_combobox(self, name: str, label: str, items: list[str], value: str='') -> InputComboBox:
        combobox = InputComboBox(name=name, label=label, items=items, value=value)
        self.input_widgets.append(combobox)
        self._add_widget(label=label, widget=combobox)
        return combobox

    def to_dict(self) -> list[dict[str, any]]:
        widgets = []
        for widget in self.input_widgets:
            widgets.append(widget.to_dict())
        return widgets

    @classmethod
    def from_dict(cls, widgets: list[dict[str, any]]):
        process_inputs = cls()

        for infos in widgets:
            widget = infos['widget']
            if widget is None:
                return

            kwargs = dict(name=infos['name'], label=infos['label'], value=infos['value'])

            if widget == 'checkbox':
                process_inputs.add_checkbox(**kwargs)
            elif widget == 'combobox':
                process_inputs.add_combobox(items=infos['items'], **kwargs)
