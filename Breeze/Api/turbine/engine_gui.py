from typing import Any, TypeVar

from PySide6 import QtCore
from PySide6.QtWidgets import QWidget, QVBoxLayout

from Api.turbine.engine_inputs import EngineInputsBase, EngineInputsBuild
from Api.turbine.utils import JobContext
from Api.turbine.gui_widgets import TurbineWidgetBase, Specifics

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

    def get_inputs(self) -> EngineInputsBase:
        """
        Returns a list of inputs with values matching those selected in the ui.
        """
        result = EngineInputsBase()
        return result

    def to_database(self) -> dict[str, Any]:
        infos = {widget.name: widget.to_dict() for widget in self.widgets}
        return infos


class EngineGuiBuild(EngineGuiBase):
    def _init_ui(self):
        self.allow_overwrite = self.add(Specifics.DontOverwrite())
        self.new_version = self.add(Specifics.NewVersion(context=self.context))
        self.version_number = self.add(Specifics.VersionNumber(context=self.context))
        self.version_number.combobox.setFixedWidth(64)

    def _connect_signals(self):
        self.new_version.checkbox.clicked.connect(self.on_last_version_clicked)

    def _init_state(self):
        self.on_last_version_clicked(is_checked=self.new_version.checkbox.isChecked())

    def on_last_version_clicked(self, is_checked: bool):
        self.version_number.setEnabled(not is_checked)

    def get_inputs(self) -> EngineInputsBuild:
        result = EngineInputsBuild(
            use_last_version=False,
            create_new_version=self.new_version.checkbox.isChecked(),
            version_number=int(self.version_number.combobox.currentText()),
            dont_overwrite=self.allow_overwrite.checkbox.isChecked(),
        )
        return result
