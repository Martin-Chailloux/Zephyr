from dataclasses import dataclass

from Api.turbine.utils import JobContext, TurbineInputsBase
from Api.turbine.gui_base import EngineGuiBase


# @dataclass
# class BlenderModelingExportInputs(TurbineInputsBase):
#     use_last_version: bool = False
#     version_number: int = None
#     dont_overwrite: bool = False


class BlenderModelingExportGui(EngineGuiBase):
    def _init_ui(self):
        # TODO: group common methods in class TurbineInputsApi
        #  - get_versions_numbers() -> str
        #  - get_selected_version_number() -> str
        #  - etc.

        # get available versions
        versions = self.context.component.versions
        versions_numbers = [version.number for version in versions]
        versions_numbers.sort(reverse=True)
        version_number_items = [f"{i:03d}" for i in versions_numbers]

        # get default inputs
        if self.context.version is None:
            selected_version_number: str = ''
        else:
            selected_version_number: str = f"{self.context.version.number:03d}"

        self.allow_overwrite = self.add_checkbox(name='allow_overwrite', label="Don't overwrite", is_checked=True)
        self.last_version = self.add_checkbox(name='last_version', label='Last version', is_checked=True)
        self.version_number = self.add_combobox(name='version_num', label='Version num', items=version_number_items, current_text=selected_version_number)
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
