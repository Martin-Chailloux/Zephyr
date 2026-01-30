from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional

from PySide6.QtCore import QObject

from Api.document_models.project_documents import Component, Version
from Api.document_models.studio_documents import User

from Utils.pills import PillModel, AbstractPills


@dataclass
class StepStatuses(AbstractPills):
    idle =       PillModel(name="idle", icon_name="mdi.dots-horizontal", color="grey")
    not_needed = PillModel(name="not_needed", icon_name="fa.minus", color="purple")
    running =    PillModel(name="running", icon_name="fa.play", color="deepskyblue")
    warning =    PillModel(name="warning", icon_name="fa.warning", color="orange")
    error =      PillModel(name="error", icon_name="fa.close", color="red")
    success =    PillModel(name="success", icon_name="fa.check", color="green")

    statuses = [idle, not_needed, running, warning, error, success]


class StepStatus(QObject):
    def __init__(self):
        super().__init__()
        self.status: PillModel = StepStatuses.idle
        self.set_idle()

    @classmethod
    def from_name(cls, name: str) -> 'StepStatus':
        status_class = cls()
        status_class.status = StepStatuses.from_name(name=name)
        return status_class

    def set_idle(self):
        self.status = StepStatuses.idle

    def set_running(self):
        self.status = StepStatuses.running

    def set_warning(self):
        self.status = StepStatuses.warning

    def set_error(self):
        self.status = StepStatuses.error

    def set_success(self):
        self.status = StepStatuses.success


@dataclass
class TurbineInputsBase:
    use_last_version: bool = True
    version_number: int = None
    dont_overwrite: bool = False


@dataclass
class JobContext:
    # NOTE: component and version are split, because a build process does not build from an existing version
    user: User
    component: Component
    version: Optional[Version]
    creation_time: datetime = field(default_factory=datetime.now)  # creation_time = datatime.now() would only update on first import

    def set_component(self, component: Component = None):
        self.component = component

    def set_version(self, version: Version):
        self.version = version
        self.component = version.component

    def set_creation_time(self):
        self.creation_time = datetime.now()

    def update_from_inputs(self, inputs: TurbineInputsBase):
        if inputs is None:
            return

        if inputs.use_last_version:
            version = self.component.get_last_version()
        elif inputs.version_number is not None:
            version = self.component.get_version(number=inputs.version_number)
        else:
            version = None

        self.set_version(version=version)
