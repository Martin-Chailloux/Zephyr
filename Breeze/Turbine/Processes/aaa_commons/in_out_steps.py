from typing import Optional

from Data.breeze_converters import get_file_instance_from_software
from Data.project_documents import Version
from Turbine.tb_core import Step
from abstract_io import AbstractSoftwareFile


class CreateFileStep(Step):
    label = "Create File"
    tooltip = "Creates a new, empty file"

    def __init__(self, version: Version):
        super().__init__()
        self.version = version
        self.file: Optional[AbstractSoftwareFile] = None

    def _inner_run(self):
        file = get_file_instance_from_software(software=self.version.software, filepath=self.version.filepath)
        self.file = file
        self.Logs.add(msg=f"Creating a {self.version.software.label} file ...")
        self.Logs.add(msg=f"'{self.version.filepath}'")
        file.new_file()

    def _is_success(self) -> bool:
        return self.file is not None


class OpenStep(Step):
    label = "Open"
    tooltip = "Opens a file"

    def __init__(self, file: AbstractSoftwareFile):
        super().__init__()
        self.set_sub_label(file.filepath)
        self.file = file

    def _inner_run(self):
        self.Logs.add(msg=f"Opening file: '{self.file.filepath}' ... ")
        self.file.open()


class SaveStep(Step):
    label = "Save"
    tooltip = "Saves the file"

    def run(self, file: AbstractSoftwareFile):
        super().run(file=file)

    def _inner_run(self, file: AbstractSoftwareFile):
        self.Logs.add(msg=f"Saving file: '{file.filepath}' ... ")
        file.save()
