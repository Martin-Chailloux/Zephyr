from dataclasses import dataclass

from PySide6 import QtCore
from PySide6.QtCore import QSize
from PySide6.QtGui import QStandardItem

from Api.document_models.project_documents import Stage
from Api.document_models.studio_documents import Software
from Gui.mvd.abstract_mvd import AbstractItemModel


@dataclass
class SoftwareItemRoles:
    software = QtCore.Qt.ItemDataRole.UserRole

@dataclass
class SoftwareItemMetrics:
    height: int = 32


class SoftwareListModel(AbstractItemModel):
    def __init__(self, stage: Stage = Stage):
        super().__init__()
        self.stage = stage
        self.populate()

    def add_item(self, software: Software):
        row = self.rowCount()

        item = QStandardItem()
        item.setSizeHint(QSize(0, SoftwareItemMetrics.height))
        item.setEditable(False)

        item.setData(software, SoftwareItemRoles.software)

        self.setItem(row, item)

    def populate(self):
        self.clear()
        for software in self.stage.stage_template.software:
            self.add_item(software)
