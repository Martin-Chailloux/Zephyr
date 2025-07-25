from dataclasses import dataclass

from Api.project_documents import JobContext
from Api.turbine.inputs_ui import ProcessInputsUi


@dataclass
class BlenderModelingExportInputs:
    dont_overwrite: bool
    last_version: bool
    version_number: int


class BlenderModelingExportUi(ProcessInputsUi):
    def __init__(self, context: JobContext = None):
        super().__init__(label='Export', context=context)
        self._init_ui()
        self._connect_signals()
        self._init_state()

    def _init_ui(self):
        versions = self.Context.component.versions

        versions_numbers = [version.number for version in versions]
        versions_numbers.sort(reverse=True)
        version_number_items = [f"{i:03d}" for i in versions_numbers]

        if self.Context.version is None:
            version_number_value = ''
            use_last_version = True
        else:
            version_number_value = f"{self.Context.version.number:03d}"
            use_last_version = False

        allow_overwrite = self.add_checkbox(name='allow_overwrite', label="Don't overwrite", is_checked=True)
        last_version = self.add_checkbox(name='last_version', label='Last version', is_checked=use_last_version)
        version_number = self.add_combobox(name='version_num', label='Version num', items=version_number_items, current_text=version_number_value)
        version_number.combobox.setFixedWidth(64)

        self.allow_overwrite = allow_overwrite
        self.last_version = last_version
        self.version_number = version_number

    def _connect_signals(self):
        self.last_version.checkbox.clicked.connect(self.on_last_version_clicked)

    def _init_state(self):
        self.on_last_version_clicked(is_checked=self.last_version.checkbox.isChecked())

    def on_last_version_clicked(self, is_checked: bool):
        self.version_number.setEnabled(not is_checked)

    @property
    def inputs(self) -> BlenderModelingExportInputs:
         return BlenderModelingExportInputs(
             dont_overwrite=self.allow_overwrite.checkbox.isChecked(),
             last_version=self.last_version.checkbox.isChecked(),
             version_number=int(self.version_number.combobox.currentText())
         )
