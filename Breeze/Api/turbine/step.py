import os
import traceback

import qtawesome
from PySide6 import QtCore
from PySide6.QtCore import Signal, QObject
from PySide6.QtWidgets import QTreeWidgetItem

from Api.turbine.pills import StepPill
from Utils.pills import PillModel
from Api.turbine.logger import StepLogger


class StepBase(QObject):
    updated = Signal()

    label: str = "step_label"
    sub_label: str = None
    tooltip: str = "step_tooltip"

    def __init__(self, sub_label: str = None):
        super().__init__()
        self.comes_from_dict: bool = False
        self.sub_label = sub_label
        self.Pill = StepPill()
        self.logger = StepLogger(name=f"{self.label}__{self.sub_label}__{os.urandom(4)}")

        self.steps: list[StepBase] = []

        self.logger.info(f"Starting step '{self.label}' ... ")
        self.log_output = ""  # used with Self.from_dict() to recover log

    def set_sub_label(self, sub_label: str):
        self.sub_label = sub_label

    @property
    def log(self):
        if self.comes_from_dict:
            return self.log_output
        else:
            return self.logger.stream.getvalue()

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

    # translators
    def to_dict(self) -> dict[str, any]:
        return StepTranslator.to_dict(step=self)

    @classmethod
    def from_dict(cls, infos: dict[str, any]) -> 'StepBase':
        return StepTranslator.from_dict(infos=infos)

    def to_tree_item(self) -> QTreeWidgetItem:
        return StepTranslator.to_tree_item(step=self)


class StepTranslator:
    @staticmethod
    def to_dict(step: StepBase) -> dict[str, any]:
        infos = {
            'label': step.label,
            'sub_label': step.sub_label,
            'tooltip': step.tooltip,
            'pill': step.pill.name,
            'log': step.log,
            'child_steps': [step.to_dict() for step in step.steps],
        }
        return infos

    @staticmethod
    def from_dict(infos: dict[str, any]) -> StepBase:
        step = StepBase(sub_label=infos['sub_label'])
        step.comes_from_dict = True
        step.label = infos['label']
        step.tooltip = infos['tooltip']
        step.Pill = StepPill.from_name(name=infos['pill'])
        step.log_output = infos['log']

        for child_step in infos['child_steps']:
            child_step = StepBase.from_dict(infos=child_step)
            step.steps.append(child_step)

        return step

    @staticmethod
    def to_tree_item(step: StepBase) -> QTreeWidgetItem:
        item = QTreeWidgetItem()

        text = step.label
        if step.sub_label is not None:
            text += f" |  {step.sub_label}"
        item.setText(0, text)

        icon = qtawesome.icon(step.pill.icon_name, color=step.pill.color)
        item.setIcon(0, icon)
        item.setData(0, QtCore.Qt.ItemDataRole.UserRole, step.log)
        return item


