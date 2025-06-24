from typing import Self
from dataclasses import dataclass

from PySide6.QtCore import Signal, QObject

from Data.project_documents import Version, MgJob, ProcessContext
from Data.studio_documents import User, MgProcess


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


class StepMessage:
    def __init__(self):
        self.msg: str = ""

    def set_msg(self, msg: str):
        self.msg = msg


class Step(QObject):
    label = "step_label"
    tooltip = "step_tooltip"
    updated = Signal()

    def __init__(self, sub_label: str=None):
        super().__init__()
        self.Pill = StepPill()
        self.Msg = StepMessage()

        self.sub_label = sub_label
        self.needed_data: list = []
        self.steps: list[Step] = []

    @property
    def pill(self) -> PillModel:
        return self.Pill.pill

    @property
    def msg(self) -> str:
        return self.Msg.msg

    def add_step(self, step: Self) -> Self:
        self.steps.append(step)
        step.updated.connect(self.on_sub_step_updated)
        return step

    def add_steps(self, steps: list[Self]):
        for step in steps:
            self.add_step(step=step)

    def set_needed_data(self, needed_data: list):
        self.needed_data = needed_data

    def on_sub_step_updated(self):
        self.updated.emit()
        print(f"STEP UPDATE: {self.label}")

    def run(self, **kwargs):
        # TODO: duration
        try:
            self._inner_run(**kwargs)
            self._resolve()
            self.updated.emit()
        except Exception as e:
            self.Msg.set_msg(str(e))
            self.Pill.set_error()
            self.updated.emit()
            raise e

    def _inner_run(self, **kwargs):
        # override with actions
        pass

    def _resolve(self):
        for data in self.needed_data:
            if data is None:
                self.Pill.set_error()
                break
        else:
            self.Pill.set_success()

    def to_dict(self) -> dict[str, any]:
        # TODO: log

        infos = {
            'label': self.label,
            'sub_label': self.sub_label,
            'tooltip': self.tooltip,
            'pill': self.pill.name,
            'msg': self.msg,
            'child_steps': [step.to_dict() for step in self.steps],
        }
        return infos


class Process(Step):
    name: str = "process_name"
    label = "process_label"
    tooltip = "process_tooltip"

    def __init__(self, user: User, version: Version):
        super().__init__()
        self.context = ProcessContext(user=user, version=version)
        self.mg_job = self.register_mg_job()
        self.Pill.set_idle()

    def run(self):
        self.Pill.set_running()
        try:
            self._inner_run()
        except Exception as e:
            pass
        self._resolve()
        self.update_mg_job()

    def on_sub_step_updated(self):
        super().on_sub_step_updated()
        self.update_mg_job()

    # ------------------------
    # process
    # ------------------------
    @classmethod
    def get_class_path(cls):
        path = f"{cls.__module__}.{cls.__qualname__}"
        return str(path)

    @classmethod
    def register_mg_process(cls):
        """ Saves the process class into the db """
        # check for duplicates
        process = MgProcess.objects(longname=cls.name)
        if process:
            raise ValueError(f"Process '{cls.name}' is already registered in the db")

        # create in db
        MgProcess.create(longname=cls.name, label=cls.label, tooltip=cls.tooltip, class_path=cls.get_class_path())

    def get_registered_mg_process(self) -> MgProcess:
        process = MgProcess.objects.get(longname=self.name, label=self.label, tooltip=self.tooltip, class_path=self.get_class_path())
        return process

    # ------------------------
    # jobs
    # ------------------------
    def register_mg_job(self) -> MgJob:
        """ Saves this instantiated process as a Job in the db"""
        process = MgJob.create(source_process=self.get_registered_mg_process(), context=self.context, steps=self.to_dict())
        return process

    def update_mg_job(self):
        """ Updates this instantiated process in the db"""
        self.mg_job.update(steps=self.to_dict())
