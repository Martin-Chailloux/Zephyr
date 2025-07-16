from dataclasses import dataclass

from PySide6 import QtCore
from PySide6.QtCore import QSize
from PySide6.QtGui import QStandardItem

from Api.studio_documents import StageTemplate
from Gui.components.mvd.abstract_mvd import AbstractListModel


@dataclass
class StageTemplateItemRoles:
    stage_template = QtCore.Qt.ItemDataRole.UserRole

@dataclass
class StageItemMetrics:
    height: int = 42
    logo_w: int = 48

class StageTemplateListModel(AbstractListModel):
    def __init__(self):
        super().__init__()
        self.stage_templates = []

    def populate(self, stage_templates: list[StageTemplate]):
        self.stage_templates = stage_templates

        self.clear()
        stage_templates = sorted(stage_templates, key=lambda x: x.order)

        for stage_template in stage_templates:
            self.add_item(stage_template=stage_template)

    def refresh(self):
        self.blockSignals(True)
        longnames = [stage_template.longname for stage_template in self.stage_templates]
        stage_templates = StageTemplate.objects(longname__in=longnames)
        self.populate(stage_templates)
        self.blockSignals(False)

    def add_item(self, stage_template: StageTemplate):
        row = self.rowCount()

        item = QStandardItem()
        item.setSizeHint(QSize(0, StageItemMetrics.height))
        item.setEditable(False)

        item.setData(stage_template, StageTemplateItemRoles.stage_template)

        self.setItem(row, item)
