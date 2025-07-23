from dataclasses import dataclass

from Api.project_documents import JobContext
from Api.turbine.inputs_ui import ProcessInputsUi


@dataclass
class BlenderModelingExportInputs:
    allow_overwrite: bool
    last_version: bool
    version_number: int


class BlenderModelingExportUi(ProcessInputsUi):
    def __init__(self, context: JobContext = None):
        super().__init__(context=context)
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

        allow_overwrite = self.add_checkbox(name='allow_overwrite', label='Allow overwrite', value=False)
        last_version = self.add_checkbox(name='last_version', label='Last version', value=use_last_version)
        version_number = self.add_combobox(name='version_num', label='Version num', items=version_number_items, value=version_number_value)
        version_number.setFixedWidth(64)

        self.allow_overwrite = allow_overwrite
        self.last_version = last_version
        self.version_number = version_number

    def _connect_signals(self):
        self.last_version.clicked.connect(self.on_last_version_clicked)

    def _init_state(self):
        self.on_last_version_clicked(is_checked=self.last_version.isChecked())

    def on_last_version_clicked(self, is_checked: bool):
        self.version_number.setEnabled(not is_checked)

    @property
    def inputs(self) -> BlenderModelingExportInputs:
         return BlenderModelingExportInputs(
             allow_overwrite=self.allow_overwrite.isChecked(),
             last_version=self.last_version.isChecked(),
             version_number=int(self.version_number.currentText())
         )