from Api.turbine.engine_inputs_widgets import Specifics
from Api.turbine.utils import TurbineInputsBase
from Api.turbine.engine_inputs_gui import EngineGuiBase


class BlenderModelingExportGui(EngineGuiBase):
    def _init_ui(self):
        self.allow_overwrite = self.add(Specifics.DontOverwrite())
        self.last_version = self.add(Specifics.LastVersion(context=self.context))
        self.version_number = self.add(Specifics.VersionNumber(context=self.context))
        self.version_number.combobox.setFixedWidth(64)

    def _connect_signals(self):
        self.last_version.checkbox.clicked.connect(self.on_last_version_clicked)

    def _init_state(self):
        self.on_last_version_clicked(is_checked=self.last_version.checkbox.isChecked())

    def on_last_version_clicked(self, is_checked: bool):
        self.version_number.setEnabled(not is_checked)

    @property
    def inputs(self) -> TurbineInputsBase:
        result = TurbineInputsBase(
            use_last_version=self.last_version.checkbox.isChecked(),
            version_number=int(self.version_number.combobox.currentText()),
            dont_overwrite=self.allow_overwrite.checkbox.isChecked(),
        )
        return result
