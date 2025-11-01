from typing import Any

from PySide6 import QtCore
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton

from Api.turbine.utils import JobContext, TurbineInputs
from Api.turbine.inputs_widgets import TurbineWidgets, TurbineWidgetBase


class TurbineGui(QWidget):
    def __init__(self, context: JobContext):
        super().__init__()
        self.context = context
        self.widgets: list[TurbineWidgetBase] = []

        layout = QVBoxLayout()
        self.setLayout(layout)
        layout.setAlignment(QtCore.Qt.AlignmentFlag.AlignTop | QtCore.Qt.AlignmentFlag.AlignLeft)
        layout.setSpacing(3)

        self.layout = layout

        self._init_ui()
        self._connect_signals()
        self._init_state()

    def _init_ui(self):
        pass

    def _connect_signals(self):
        pass

    def _init_state(self):
        pass

    # add widgets
    def add_checkbox(self, name: str, label: str, is_checked: bool=False) -> TurbineWidgets.Checkbox:
        checkbox = TurbineWidgets.Checkbox(name=name, label=label, is_checked=is_checked)
        self.widgets.append(checkbox)
        self.layout.addWidget(checkbox)
        return checkbox

    def add_combobox(self, name: str, label: str, items: list[str], current_text: str='') -> TurbineWidgets.Combobox:
        combobox = TurbineWidgets.Combobox(name=name, label=label, items=items, current_text=current_text)
        self.widgets.append(combobox)
        self.layout.addWidget(combobox)
        return combobox

    @property
    def inputs(self) -> TurbineInputs:
        """
        Returns a list of inputs with values matching those selected in the ui.
        """
        result = TurbineInputs()
        return result

    def to_database(self) -> dict[str, Any]:
        infos = {widget.name: widget.export_infos() for widget in self.widgets}
        return infos

    # @classmethod
    # def from_dict(cls, widgets: list[dict[str, any]]):
    #     process_inputs = cls()
    #
    #     for infos in widgets:
    #         widget_type = infos['widget']
    #         if widget_type is None:
    #             return
    #
    #         name=infos['name']
    #         label=infos['label']
    #
    #         if widget_type == 'checkbox':
    #             process_inputs.add_checkbox(name=name, label=label, is_checked=infos.get('is_checked', False))
    #         elif widget_type == 'combobox':
    #             process_inputs.add_combobox(name=name, label=label, items=infos.get('items', []), current_text=infos.get('current_text', ''))
