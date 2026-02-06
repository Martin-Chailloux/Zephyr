from typing import Any, TypeVar

from PySide6 import QtCore
from PySide6.QtWidgets import QWidget, QVBoxLayout

from Api.turbine.utils import JobContext, InputsBase
from Api.turbine.gui_widgets import TurbineWidgetBase

TWidget = TypeVar("TWidget", bound=TurbineWidgetBase)


class GuiBase(QWidget):
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

        self._before_init_ui()
        self._init_ui()

        self._before_connect_signals()
        self._connect_signals()

        self._before_init_state()
        self._init_state()

    def _before_init_ui(self):
        """ hook """
        pass

    def _init_ui(self):
        pass

    def _before_connect_signals(self):
        """ hook """
        pass

    def _connect_signals(self):
        pass

    def _before_init_state(self):
        """ hook """
        pass

    def _init_state(self):
        pass

    def add(self, widget: TWidget):
        self.widgets.append(widget)
        self.layout.addWidget(widget)
        return widget

    def get_inputs(self) -> InputsBase:
        """
        Returns a list of inputs with values matching those selected in the ui.
        """
        result = InputsBase()
        return result

    def export_inputs(self) -> dict[str, Any]:
        infos = {widget.name: widget.export_config() for widget in self.widgets}
        return infos

    def import_inputs(self, inputs: dict[str, Any]):
        for widget in self.widgets:
            infos: dict[str, any] = inputs.get(widget.name, None)
            if infos is not None:
                widget.import_config(**infos)
        self._init_state()
