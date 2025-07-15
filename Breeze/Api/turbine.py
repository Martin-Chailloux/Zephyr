import logging
import os
import traceback
from dataclasses import dataclass
from io import StringIO

from PySide6.QtCore import Signal, QObject

from Api.project_documents import Version, Job, JobContext, Component
from Api.studio_documents import User, Process, Software


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


class StepLogger:
    def __init__(self, name: str):
        stream = StringIO()
        formatter = logging.Formatter('%(asctime)s - %(levelname)-8s: %(message)s', datefmt='%H:%M:%S')

        handler = logging.StreamHandler()
        handler.setStream(stream)
        handler.setLevel(logging.DEBUG)
        handler.setFormatter(formatter)

        logger = logging.getLogger(name)
        logger.setLevel(logging.DEBUG)
        if logger.hasHandlers():
            logger.handlers.clear()
        logger.addHandler(handler)

        self.logger = logger
        self.stream = stream

    def info(self, msg: str):
        self.logger.info(msg)

    def debug(self, msg: str):
        self.logger.debug(msg)

    def warning(self, msg: str):
        self.logger.warning(msg)

    def error(self, msg: str):
        self.logger.error(msg)

    def critical(self, msg: str):
        self.logger.critical(msg)

    @property
    def output(self) -> str:
        return self.stream.getvalue()


class StepBase(QObject):
    updated = Signal()

    label: str = "step_label"
    sub_label: str = None
    tooltip: str = "step_tooltip"

    def __init__(self, sub_label: str = None):
        super().__init__()
        self.sub_label = sub_label
        self.Pill = StepPill()
        self.logger = StepLogger(name=f"{self.label}__{self.sub_label}__{os.urandom(4)}")

        self.steps: list[StepBase] = []

        self.logger.info(f"Starting step '{self.label}' ... ")

    def set_sub_label(self, sub_label: str):
        self.sub_label = sub_label

    @property
    def pill(self) -> PillModel:
        return self.Pill.pill

    def add_step(self, step: 'StepBase') -> 'StepBase':
        self.steps.append(step)
        step.updated.connect(self.on_sub_step_updated)
        return step

    def add_steps(self, steps: list['StepBase']):
        for step in steps:
            self.add_step(step=step)

    def on_sub_step_updated(self):
        self.updated.emit()

    def run(self, **kwargs):
        # TODO: duration

        self.Pill.set_running()
        try:
            self._inner_run(**kwargs)
            self._resolve()
            self.updated.emit()
            self.logger.info(msg=f"... step '{self.label}': SUCCESS \n")

        except Exception as e:
            self.logger.error(msg=traceback.format_exc())
            self.Pill.set_error()
            self.updated.emit()
            raise RuntimeError(traceback.format_exc(chain=False))

    def _inner_run(self, **kwargs):
        # override with actions
        pass

    @property
    def _is_success(self) -> bool:
        return True

    def _resolve(self):
        if self._is_success:
            self.Pill.set_success()
        else:
            self.Pill.set_error()

    def to_dict(self) -> dict[str, any]:
        infos = {
            'label': self.label,
            'sub_label': self.sub_label,
            'tooltip': self.tooltip,
            'pill': self.pill.name,
            'log': self.logger.output,
            'child_steps': [step.to_dict() for step in self.steps],
        }
        return infos


class StepLabel(StepBase):
    def __init__(self, label: str, sub_label: str = None):
        self.label = label
        super().__init__(sub_label = sub_label)

    def set_done(self):
        super().run()


class ProcessBase(StepBase):
    name: str = "process_name"
    label = "process_label"
    tooltip = "process_tooltip"

    def __init__(self, user: User, component: Component, version: Version = None):
        # component and version are split for build process where the component may have 0 versions
        super().__init__()
        self.Context = JobContext(user=user, component=component, version=version)
        self.mg_job = self.register_mg_job()
        self.Pill.set_idle()

    def run(self):
        self.Pill.set_running()

        try:
            super().run()
            self.Pill.set_success()
        except RuntimeError:
            print(f"{self.label = }")
            print(traceback.format_exc(chain=False))
            self.Pill.set_error()

        self.update_mg_job()

    def on_sub_step_updated(self):
        super().on_sub_step_updated()
        self.update_mg_job()

    def set_source_version(self, version: Version = None):
        self.mg_job.update(source_version = version)
        self.Context.set_version(version=version)

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
        process = Process.objects(longname=cls.name)
        if process:
            process = process[0]
            process.update(label=cls.label, tooltip=cls.tooltip, class_path=cls.get_class_path())

        # create in db
        Process.create(longname=cls.name, label=cls.label, tooltip=cls.tooltip, class_path=cls.get_class_path())

    def get_registered_mg_process(self) -> Process:
        process = Process.objects.get(longname=self.name, label=self.label, tooltip=self.tooltip, class_path=self.get_class_path())
        return process

    # ------------------------
    # jobs
    # ------------------------
    def register_mg_job(self) -> Job:
        """ Saves this instantiated process as a Job in the db"""
        process = Job.create(source_process=self.get_registered_mg_process(), context=self.Context, steps=self.to_dict())
        return process

    def update_mg_job(self):
        """ Updates this instantiated process in the db"""
        self.mg_job.update(steps=self.to_dict())
