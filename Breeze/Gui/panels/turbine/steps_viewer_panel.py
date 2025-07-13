from dataclasses import dataclass

import qtawesome
from PySide6 import QtCore
from PySide6.QtCore import Signal
from PySide6.QtWidgets import QTreeWidget, QTreeWidgetItem

from Api.project_documents import Job
from Api.turbine import Pills, PillModel


@dataclass
class Translators:
    name_to_pill = {
        'idle': Pills.idle,
        'error': Pills.error,
        'running': Pills.running,
        'warning': Pills.warning,
        'not_needed': Pills.not_needed,
        'success': Pills.success,
    }


class StepsViewer(QTreeWidget):
    step_selected = Signal(dict)

    def __init__(self):
        super().__init__()
        self._connect_signals()

    def populate(self, job: Job):
        # TODO: create a property in the document that returns the step with dot notation
        #  (or instead find a field that does it)
        #  (edit: NO) or just add a translator here, it might be enough
        self.clear()
        main_step = job.steps

        top_item = QTreeWidgetItem()
        top_item.setText(0, main_step['label'])
        self.addTopLevelItem(top_item)

        for step in main_step['child_steps']:
            self.add_step(parent=top_item, step=step)

        self.expandAll()

    def add_step(self, parent: QTreeWidgetItem, step: dict):
        item = QTreeWidgetItem()
        text = step['label']
        sub_label = step.get('sub_label', None)
        if sub_label is not None:
            text += f" |  {sub_label}"
        item.setText(0, text)
        pill: PillModel = Translators.name_to_pill[step['pill']]
        icon = qtawesome.icon(pill.icon_name, color=pill.color)
        item.setIcon(0, icon)
        item.setData(0, QtCore.Qt.ItemDataRole.UserRole, step)
        parent.addChild(item)
        for step in step['child_steps']:
            self.add_step(parent=item, step=step)

    def _connect_signals(self):
        self.selectionModel().selectionChanged.connect(self.on_selection_changed)

    def on_selection_changed(self):
        items = self.selectedItems()
        if not items:
            return
        step = items[0].data(0, QtCore.Qt.ItemDataRole.UserRole)
        self.step_selected.emit(step)