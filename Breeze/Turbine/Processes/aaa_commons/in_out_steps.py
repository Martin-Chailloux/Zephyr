from typing import Optional

from Data.breeze_converters import get_file_instance_from_software
from Data.project_documents import Version, Component
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
        template_component = Component.objects.get(longname='Templates_startup_Blender_modeling_work')
        source_version = template_component.get_last_version()
        self.Logs.add(f"{source_version = }")

        file = get_file_instance_from_software(software=source_version.software, filepath=source_version.filepath)
        file.open()
        file.save_as(filepath=self.version.filepath)
        self.file = file
        self.Logs.add(msg=f"Creating a {self.version.software.label} file ...")
        self.Logs.add(msg=f"{self.version = }")
        # file.new_file()

    def _is_success(self) -> bool:
        return self.file is not None


class OpenStep(Step):
    label = "Open"
    tooltip = "Opens a file"

    def __init__(self, version: Version):
        super().__init__()
        self.version = version
        self.file: Optional[str] = None

    def _is_success(self) -> bool:
        return self.file is not None

    def _inner_run(self):
        self.Logs.add(msg=f"Opening version: '{self.version}' ... ")
        self.file = self.version.to_file()
        self.file.open()


class SaveStep(Step):
    label = "Save"
    tooltip = "Saves the file"

    def run(self, file: AbstractSoftwareFile):
        super().run(file=file)

    def _inner_run(self, file: AbstractSoftwareFile):
        self.Logs.add(msg=f"Saving file: '{file.filepath}' ... ")
        file.save()
