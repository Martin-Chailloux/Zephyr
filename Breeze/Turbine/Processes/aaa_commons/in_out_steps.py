from typing import Optional

from Data.project_documents import Version, Component
from Turbine.tb_core import Step
from abstract_io import AbstractSoftwareFile


class CreateFileStep(Step):
    label = "Create File"
    tooltip = "Creates a new, empty file"

    def __init__(self, version: Version):
        super().__init__()
        self.version = version
        print(f"{self.version = }")
        self.file: Optional[AbstractSoftwareFile] = None

    def _inner_run(self):
        template_component: Component = Component.objects.get(longname='Templates_startup_Blender_modeling_work')
        print(f"{template_component = }")
        source_version = template_component.get_last_version()
        if source_version is None:
            raise ValueError(f"No versions were found in the template component {template_component.__repr__()}")
        print(f"{source_version = }")
        self.Logs.add(f"{source_version = }")

        file = source_version.to_file()
        file.save_as(filepath=self.version.filepath)
        self.file = file
        self.Logs.add(msg=f"Creating a {self.version.software.label} file ...")
        self.Logs.add(msg=f"{self.version = }")

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
