from typing import Optional

import bpy

from Api.project_documents import Version
from Api.turbine.step import StepBase
from blender_file import BlenderFile


class CollectStep(StepBase):
    label: str = "Collect"
    tooltip: str = ""

    def __init__(self):
        super().__init__()
        self.export_collection = None

    def _is_success(self) -> bool:
        return self.export_collection is not None

    def _inner_run(self):
        self.export_collection = bpy.data.collections.get('Export', None)


class ExportStep(StepBase):
    label: str = "Export"
    tooltip: str = ""

    def __init__(self, version: Version, allow_overwrite: bool):
        super().__init__()
        self.source_version = version
        self.allow_overwrite = allow_overwrite
        self.file: Optional[BlenderFile] = None

    def _is_success(self) -> bool:
        return self.file is not None

    def _inner_run(self):
        # create component
        self.file = self.source_version.to_file()
        self.file.open()

        component = self.source_version.component.stage.create_component(name="geo", label="Geo", crash_if_exists=False)  # TODO: create should not get, split in 2
        version = component.get_version(number=self.source_version.number)
        if version is None:
            version = component.create_version(number=self.source_version.number, software=self.source_version.software)
        elif not self.allow_overwrite:
            raise ValueError(f"Version {version.__repr__()} already exists. Use 'allow overwrite' to export over it.")
        else:
            self.logger.debug(f"Overriding an existing version: {self.allow_overwrite = }")


        self.file.save_as(filepath=version.filepath)
