from dataclasses import dataclass

import qtawesome
from PySide6.QtWidgets import QTreeWidget, QTreeWidgetItem

from Data.project_documents import Job
from Turbine.tb_core import Pills, PillModel


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
    def __init__(self):
        super().__init__()

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
        item.setText(0, step['label'])
        pill: PillModel = Translators.name_to_pill[step['pill']]
        icon = qtawesome.icon(pill.icon_name, color=pill.color)
        item.setIcon(0, icon)
        parent.addChild(item)
        for step in step['child_steps']:
            self.add_step(parent=item, step=step)
