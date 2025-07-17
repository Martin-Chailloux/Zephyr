from dataclasses import dataclass

from PySide6.QtCore import QObject


@dataclass
class PillModel:
    name: str
    icon_name: str
    color: str

    def __repr__(self):
        return f"<StepPill> {self.name}"


@dataclass
class Pills:
    idle =       PillModel(name="idle", icon_name="mdi.dots-horizontal", color="grey")
    not_needed = PillModel(name="not_needed", icon_name="fa.minus", color="purple")
    running =    PillModel(name="running", icon_name="fa.play", color="deepskyblue")
    warning =    PillModel(name="warning", icon_name="fa.warning", color="orange")
    error =      PillModel(name="error", icon_name="fa.close", color="red")
    success =    PillModel(name="success", icon_name="fa.check", color="green")


class StepPill(QObject):
    def __init__(self):
        super().__init__()
        self.pill: PillModel = Pills.idle
        self.set_idle()

    def set_idle(self):
        self.pill = Pills.idle

    def set_running(self):
        self.pill = Pills.running

    def set_warning(self):
        self.pill = Pills.warning

    def set_error(self):
        self.pill = Pills.error

    def set_success(self):
        self.pill = Pills.success

    @classmethod
    def from_name(cls, name: str) -> 'StepPill':
        translator = {
        'idle': Pills.idle,
        'error': Pills.error,
        'running': Pills.running,
        'warning': Pills.warning,
        'not_needed': Pills.not_needed,
        'success': Pills.success,
        }

        step_pill = cls()
        step_pill.pill = translator[name]
        return step_pill
