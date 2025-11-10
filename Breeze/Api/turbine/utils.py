from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional

from PySide6.QtCore import QObject

from Api.document_models.project_documents import Component, Version
from Api.document_models.studio_documents import User

from Utils.pills import PillModel, AbstractPills


@dataclass
class StepPills(AbstractPills):
    idle =       PillModel(name="idle", icon_name="mdi.dots-horizontal", color="grey")
    not_needed = PillModel(name="not_needed", icon_name="fa.minus", color="purple")
    running =    PillModel(name="running", icon_name="fa.play", color="deepskyblue")
    warning =    PillModel(name="warning", icon_name="fa.warning", color="orange")
    error =      PillModel(name="error", icon_name="fa.close", color="red")
    success =    PillModel(name="success", icon_name="fa.check", color="green")

    pills = [idle, not_needed, running, warning, error, success]


class StepPill(QObject):
    def __init__(self):
        super().__init__()
        self.pill: PillModel = StepPills.idle
        self.set_idle()

    @classmethod
    def from_name(cls, name: str) -> 'StepPill':
        step_pill = cls()
        step_pill.pill = StepPills.from_name(name=name)
        return step_pill

    def set_idle(self):
        self.pill = StepPills.idle

    def set_running(self):
        self.pill = StepPills.running

    def set_warning(self):
        self.pill = StepPills.warning

    def set_error(self):
        self.pill = StepPills.error

    def set_success(self):
        self.pill = StepPills.success


@dataclass
class JobContext:
    # NOTE: component and version are split, because a build process may use a component with 0 versions in it
    user: User
    component: Component
    version: Optional[Version]
    creation_time: datetime = field(default_factory=datetime.now)  # creation_time = datatime.now() would only update on first import

    def set_component(self, component: Component = None):
        self.component = component

    def set_version(self, version: Version = None):
        self.version = version
        self.component = version.component

    def update_creation_time(self):
        self.creation_time = datetime.now()

@dataclass
class TurbineInputs:
    use_last_version: bool = True
    version_number: int = None
