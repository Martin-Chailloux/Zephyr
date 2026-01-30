from typing import Any, TypeVar

from PySide6 import QtCore
from PySide6.QtWidgets import QWidget, QVBoxLayout

from Api.turbine.utils import JobContext, TurbineInputsBase
from Api.turbine.inputs_widgets import TurbineWidgets, TurbineWidgetBase


class EngineGuiBase(QWidget):
    def __init__(self, context: JobContext):
        """
        Creates the inputs layout
        :param context: context of the gui's creation ; used to preset the inputs
        """
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
    def inputs(self) -> TurbineInputsBase:
        """
        Returns a list of inputs with values matching those selected in the ui.
        """
        result = TurbineInputsBase()
        return result

    def to_database(self) -> dict[str, Any]:
        infos = {widget.name: widget.export_infos() for widget in self.widgets}
        return infos
