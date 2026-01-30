import importlib
import os
import traceback
from typing import TypeVar, Optional, Generic, Type, Self

import qtawesome
from PySide6 import QtCore
from PySide6.QtCore import Signal, QObject
from PySide6.QtWidgets import QTreeWidgetItem

from Api.document_models.project_documents import Job
from Api.document_models.studio_documents import Process
from Api.turbine.gui_base import EngineGuiBase
from Api.turbine.utils import StepStatus, JobContext, TurbineInputsBase
from Api.turbine.logger import StepLogger

from Utils.pills import PillModel


TStep = TypeVar("TStep", bound='TurbineStep')


class TurbineStep(QObject):
    """
    Multiple steps are assembled inside a TurbineEngine and ran after each other.
    """

    updated = Signal()
    label: str = "label"
    sub_label: str = None
    tooltip: str = "tooltip"

    def __init__(self, sub_label: str = None):
        super().__init__()
        self.comes_from_dict: bool = False  # used with logs
        self.sub_label: str = sub_label
        self.Pill: StepStatus = StepStatus()
        self.logger: StepLogger = StepLogger(name=f"{self.label}__{self.sub_label}__{os.urandom(4)}")

        self.steps: list[TurbineStep] = []
        self.engine: Optional[TurbineEngine] = None

        self.logger.info(f"Starting step '{self.label}' ... ")
        self.log_output = ""  # used with Self.from_dict() to recover log

    def set_sub_label(self, sub_label: str):
        self.sub_label = sub_label

    def get_log(self) -> str:
        if self.comes_from_dict:
            return self.log_output
        else:
            return self.logger.stream.getvalue()

    @property
    def pill(self) -> PillModel:
        return self.Pill.status

    def set_engine(self, engine: 'TurbineEngine'):
        self.engine = engine

    def add_step(self, step: TStep) -> TStep:
        self.steps.append(step)
        step.set_engine(engine=self.engine)
        step.updated.connect(self.on_sub_step_updated)
        return step

    def add_group(self, label: str, sub_label: str = None) -> 'StepGroup':
        step_group = self.add_step(StepGroup(label=label, sub_label=sub_label))
        return step_group

    def on_sub_step_updated(self):
        self.updated.emit()

    def run(self, **kwargs):
        # TODO: duration

        self.Pill.set_running()
        try:
            self._inner_run(**kwargs)
            self.set_success()

        except Exception as e:
            self.set_failed()

    def _inner_run(self, **kwargs):
        # override with actions
        pass

    def set_success(self):
        self.updated.emit()
        self.logger.info(msg=f"... step '{self.label}': SUCCESS \n")
        self.Pill.set_success()

    def set_failed(self):
        self.logger.error(msg=traceback.format_exc())
        self.Pill.set_error()
        self.updated.emit()
        raise RuntimeError(traceback.format_exc(chain=False))

    # translators
    def to_dict(self) -> dict[str, any]:
        return StepTranslator.to_dict(step=self)

    @classmethod
    def from_dict(cls, infos: dict[str, any]) -> 'TurbineStep':
        return StepTranslator.from_dict(infos=infos)

    def to_tree_item(self) -> QTreeWidgetItem:
        return StepTranslator.to_tree_item(step=self)


class StepGroup(TurbineStep):
    def __init__(self, label: str, sub_label: str = None):
        self.label = label
        super().__init__(sub_label = sub_label)


class StepTranslator:
    @staticmethod
    def to_dict(step: TurbineStep) -> dict[str, any]:
        infos = {
            'label': step.label,
            'sub_label': step.sub_label,
            'tooltip': step.tooltip,
            'pill': step.pill.name,
            'log': step.get_log(),
            'child_steps': [step.to_dict() for step in step.steps],
        }
        return infos

    @staticmethod
    def from_dict(infos: dict[str, any]) -> TurbineStep:
        step = TurbineStep(sub_label=infos['sub_label'])
        step.comes_from_dict = True
        step.label = infos['label']
        step.tooltip = infos['tooltip']
        step.Pill = StepStatus.from_name(name=infos['pill']) # TODO: rename 'pill' with 'status'
        step.log_output = infos['log']

        for child_step in infos['child_steps']:
            child_step = TurbineStep.from_dict(infos=child_step)
            step.steps.append(child_step)

        return step

    @staticmethod
    def to_tree_item(step: TurbineStep) -> QTreeWidgetItem:
        item = QTreeWidgetItem()

        text = step.label
        if step.sub_label is not None:
            text += f" |  {step.sub_label}"
        item.setText(0, text)

        icon = qtawesome.icon(step.pill.icon_name, color=step.pill.color)
        item.setIcon(0, icon)
        item.setData(0, QtCore.Qt.ItemDataRole.UserRole, step.get_log())
        return item


TGui = TypeVar("TGui", bound=EngineGuiBase)

class TurbineEngine(TurbineStep, Generic[TGui]):
    """
    Series of step that from a process. Examples: Build, Export, Review, etc ...
    """

    name: str = "process_name"
    label: str = "process_label"
    tooltip: str = "process_tooltip"
    Gui: Type[TGui]

    @classmethod
    def from_database(cls, process: Process, context: JobContext) -> Self:
        """ Returns the instance of TurbineEngine that matches the given process """
        module_path, class_name = process.class_path.rsplit('.', 1)
        try:
            module = importlib.import_module(module_path)
        except:
            raise ValueError(f"module not found from path {module_path}")
        Engine: Type[Self] = getattr(module, class_name)
        engine = Engine(context=context)
        return engine

    def __init__(self, context: JobContext):
        super().__init__(sub_label=None)
        self.context = context
        self.engine = self  # memory leak ? caution, easy to fix anyway
        # self.gui: TGui = self.Gui(context=context)
        self.gui: TGui[EngineGuiBase] = self.Gui(context=context)
        self.refresh_context()
        self.job: Optional[Job] = None

    def refresh_context(self):
        self.context.update_from_inputs(inputs=self.gui.inputs)

    def _before_run(self):
        """ hook, currently used in build engines """
        pass

    def set_gui(self, gui: EngineGuiBase):
        self.gui = gui

    def _add_steps(self):
        """ Add steps here rather than during init so that inputs can be updated in-between """
        pass

    def run(self):
        self.job = self.create_job()
        self._before_run()
        self._add_steps()
        self.Pill.set_idle()

        self.logger.debug(f"{self.gui.inputs = }")
        self.Pill.set_running()

        try:
            super().run()
            self.Pill.set_success()
        except RuntimeError:
            print(f"{self.label = }")
            print(traceback.format_exc(chain=False))
            self.Pill.set_error()

        self.update_job()

    def on_sub_step_updated(self):
        super().on_sub_step_updated()
        self.update_job()

    # ------------------------
    # process
    # ------------------------
    @classmethod
    def get_class_path(cls) -> str:
        path = f"{cls.__module__}.{cls.__qualname__}"
        return str(path)

    @classmethod
    def register(cls):
        """ Create the Process in the database, or update it if it exists """
        process = cls.get_related_process()
        if process is None:
            Process.create(longname=cls.name, class_path=cls.get_class_path(), label=cls.label, tooltip=cls.tooltip)
        else:
            process.update(class_path=cls.get_class_path(), label=cls.label, tooltip=cls.tooltip)

    @classmethod
    def get_related_process(cls) -> Process | None:
        process = Process.objects(longname=cls.name)
        if process:
            return process[0]
        else:
            return None

    # ------------------------
    # jobs
    # ------------------------
    def create_job(self) -> Job:
        """ Saves this engine's run as a Job in the db"""
        # self.register()  # ?, not needed but nice safe measure
        source_process = Process.objects.get(longname=self.name, label=self.label, tooltip=self.tooltip, class_path=self.get_class_path())

        job = Job.create(source_process=source_process,
                         steps=self.to_dict(),
                         inputs=self.gui.to_database(),
                         user=self.context.user,
                         version=self.context.version,
                         creation_time=self.context.creation_time)
        return job

    def update_job(self):
        """ Updates the current job """
        self.job.update(steps=self.to_dict())


class BuildEngineBase(TurbineEngine, Generic[TGui]):
    # TODO: when a build fails, show it clearly in the ui
    #  changing the display of file-less versions might do the trick
    #  (and any invalid version)
    def _before_run(self):
        built_version = self.context.component.create_last_version()
        built_version.set_comment(text='Build')
        self.job.update(source_version=built_version)
        self.context.set_version(version=built_version)
        self.logger.info(f"Creating built version... {built_version}")
