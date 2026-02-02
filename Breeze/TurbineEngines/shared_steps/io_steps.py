from typing import TypeVar

from Api.document_models.project_documents import Version
from Api.turbine.step import TurbineStep
from software_base import AbstractSoftwareFile


File = TypeVar("File")


class OpenStep(TurbineStep):
    label = "Open"
    tooltip = "Open a file from a version"

    def __init__(self):
        super().__init__()
        self.file: File = None

    def run(self, version: Version):
        super().run(version=version)

    def _inner_run(self, version: Version):
        self.set_sub_label(version.longname)
        self.logger.info(msg=f"Opening a file from version: {version} ...")
        self.logger.debug(msg=f"{version.filepath = }")
        file = version.to_file()
        file.open()
        self.file = file


class SaveStep(TurbineStep):
    label = "Save"
    tooltip = "Saves the file"

    def run(self, file: AbstractSoftwareFile):
        super().run(file=file)

    def _inner_run(self, file: AbstractSoftwareFile):
        self.logger.info(msg=f"Saving file: '{file.filepath}' ... ")
        file.save()


class SaveAsStep(TurbineStep):
    label = "Save As"
    tooltip = "Saves a file in an other version"

    def __init__(self):
        super().__init__()
        self.file: [AbstractSoftwareFile] = None

    def run(self, file: AbstractSoftwareFile, target_version: Version):
        super().run(file=file, target_version=target_version)

    def _inner_run(self, file: AbstractSoftwareFile, target_version: Version):
        self.logger.info(msg=f"Saving file: '{file.filepath}' in version: {target_version} ... ")
        file.save_as(filepath=target_version.filepath)
        self.file = file
        self.set_sub_label(target_version.__repr__())


class ReserveExportVersionStep(TurbineStep):
    label: str = "Reserve export Version"
    tooltip: str = ""

    def __init__(self, source_version: Version, component_name: str, extension: str):
        super().__init__()
        self._source_version = source_version
        self._name = component_name
        self._extension = extension

    def _inner_run(self):
        component = self._source_version.component.stage.create_or_get_component(name=self._name, extension=self._extension, crash_if_exists=False)
        self.logger.debug(f"{component = }")

        version = component.get_version(number=self._source_version.number)
        if version is None:
            version = component.create_version(number=self._source_version.number)
        else:
            self.logger.debug(f"Overriding an existing version ...")
            if self.engine.gui.get_inputs().dont_overwrite:
                raise FileExistsError(f"{version} already exists. Uncheck 'don't overwrite' to overwrite it.")
        self.version = version
