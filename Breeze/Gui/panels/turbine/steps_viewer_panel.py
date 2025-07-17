from PySide6 import QtCore
from PySide6.QtCore import Signal
from PySide6.QtWidgets import QTreeWidget, QTreeWidgetItem

from Api.project_documents import Job
from Api.turbine.step import StepBase


class StepsViewer(QTreeWidget):
    step_selected = Signal()

    def __init__(self):
        super().__init__()
        self._connect_signals()

    def populate(self, job: Job):
        self.clear()

        main_step = StepBase.from_dict(infos=job.steps)
        top_item = main_step.to_tree_item()
        self.addTopLevelItem(top_item)

        for step in main_step.steps:
            self.add_step(parent=top_item, step=step)

        self.expandAll()

    def add_step(self, parent: QTreeWidgetItem, step: StepBase):
        item = step.to_tree_item()
        parent.addChild(item)

        for step in step.steps:
            self.add_step(parent=item, step=step)

    def _connect_signals(self):
        self.selectionModel().selectionChanged.connect(self.on_selection_changed)

    def on_selection_changed(self):
        self.step_selected.emit()

    @property
    def selected_step_log(self) -> str:
        items = self.selectedItems()
        if not items:
            return ""
        else:
            log = items[0].data(0, QtCore.Qt.ItemDataRole.UserRole)
            return log
