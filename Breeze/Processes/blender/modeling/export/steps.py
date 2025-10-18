from typing import Optional

import bpy

from Api.document_models.project_documents import Version
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
        self.logger.debug(f"{self.export_collection = }")


class ExportStep(StepBase):
    label: str = "Export"
    tooltip: str = ""

    def __init__(self, version: Version, dont_overwrite: bool):
        super().__init__()
        self.source_version = version
        self.dont_overwrite = dont_overwrite
        self.file: Optional[BlenderFile] = None

    def _is_success(self) -> bool:
        return self.file is not None

    def _inner_run(self):
        self.file = self.source_version.to_file()
        self.file.open()

        component = self.source_version.component.stage.create_component(name="geo", label="Geo", crash_if_exists=False)
        version = component.get_version(number=self.source_version.number)
        if version is None:
            version = component.create_version(number=self.source_version.number, software=self.source_version.software)
        elif self.dont_overwrite:
            raise ValueError(f"Version {version.__repr__()} already exists. Uncheck `don't overwrite` to export over it.")
        else:
            self.logger.debug(f"Overriding an existing version: {self.dont_overwrite = }")

        self.file.save_as(filepath=version.filepath)
