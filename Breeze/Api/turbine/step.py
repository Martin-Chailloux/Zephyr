import os
import traceback
from typing import TypeVar

import qtawesome
from PySide6 import QtCore
from PySide6.QtCore import Signal, QObject
from PySide6.QtWidgets import QTreeWidgetItem

from Api.turbine.utils import StepPill
from Utils.pills import PillModel
from Api.turbine.logger import StepLogger


TypeTurbineStep = TypeVar("TypeTurbineStep")


class TurbineStep(QObject):
    """
    Multiple steps are assembled inside a TurbineEngine and ran after each other.
    """

    updated = Signal()
    label: str = "step_label"
    sub_label: str = None
    tooltip: str = "step_tooltip"

    def __init__(self, sub_label: str = None):
        super().__init__()
        self.comes_from_dict: bool = False
        self.sub_label: str = sub_label
        self.Pill: StepPill = StepPill()
        self.logger: StepLogger = StepLogger(name=f"{self.label}__{self.sub_label}__{os.urandom(4)}")

        self.steps: list[TurbineStep] = []

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
        return self.Pill.pill

    def add_step(self, step: TypeTurbineStep) -> TypeTurbineStep:
        self.steps.append(step)
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
        step.Pill = StepPill.from_name(name=infos['pill'])
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
