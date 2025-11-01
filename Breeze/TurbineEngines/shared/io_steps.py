from typing import Optional

from Api.document_models.project_documents import Version
from Api.turbine.step import TurbineStep
from abstract_io import AbstractSoftwareFile


class OpenStep(TurbineStep):
    label = "Open Step"
    tooltip = "Open a file from a version"

    def __init__(self):
        super().__init__()
        self.file: Optional[AbstractSoftwareFile] = None

    def run(self, version: Version):
        super().run(version=version)

    def _inner_run(self, version: Version):
        self.logger.info(msg=f"Opening a file from version: {version} ...")
        self.logger.debug(msg=f"{version.filepath = }")
        file = version.to_file()
        file.open()
        self.file = file
        self.set_sub_label(version.longname)


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
