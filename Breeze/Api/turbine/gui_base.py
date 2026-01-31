from typing import Any, TypeVar

from PySide6 import QtCore
from PySide6.QtWidgets import QWidget, QVBoxLayout

from Api.turbine.utils import JobContext, TurbineInputsBase
from Api.turbine.inputs_widgets import TurbineWidgets, TurbineWidgetBase




TWidget = TypeVar("TWidget", bound=TurbineWidgetBase)

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

    def add(self, widget: TWidget):
        self.widgets.append(widget)
        self.layout.addWidget(widget)
        return widget

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
