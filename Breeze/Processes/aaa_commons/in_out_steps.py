from typing import Optional

from Api.project_documents import Version
from Api.turbine.step import StepBase
from abstract_io import AbstractSoftwareFile


class StepLabel(StepBase):
    def __init__(self, label: str, sub_label: str = None):
        self.label = label
        super().__init__(sub_label = sub_label)

    def set_done(self):
        super().run()


class OpenStep(StepBase):
    label = "Open Step"
    tooltip = "Open a file from a version"

    def __init__(self):
        super().__init__()
        self.version: Optional[Version] = None
        self.file: Optional[AbstractSoftwareFile] = None

    def _is_success(self) -> bool:
        for x in [self.version, self.file]:
            if x is None:
                return False
        else:
            return True

    def run(self, version: Version):
        super().run(version=version)

    def _inner_run(self, version: Version):
        self.logger.info(msg=f"Opening a file from version: {version.__repr__()} ...")
        self.logger.info(msg=f"{version.filepath = }")
        file = version.to_file()
        file.open()
        self.version = version
        self.file = file
        self.set_sub_label(self.version.longname)


class SaveStep(StepBase):
    label = "Save"
    tooltip = "Saves the file"

    def run(self, file: AbstractSoftwareFile):
        super().run(file=file)

    def _inner_run(self, file: AbstractSoftwareFile):
        self.logger.info(msg=f"Saving file: '{file.filepath}' ... ")
        file.save()


class SaveAsStep(StepBase):
    label = "Save As"
    tooltip = "Saves a file in an other version"

    def __init__(self):
        super().__init__()
        self.file: [AbstractSoftwareFile] = None

    def _is_success(self) -> bool:
        return self.file is not None

    def run(self, file: AbstractSoftwareFile, target_version: Version):
        super().run(file=file, target_version=target_version)

    def _inner_run(self, file: AbstractSoftwareFile, target_version: Version):
        self.logger.info(msg=f"Saving file: '{file.filepath}' in version: {target_version.__repr__()} ... ")
        file.save_as(filepath=target_version.filepath)
        self.file = file
        self.set_sub_label(target_version.longname)
